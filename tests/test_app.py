import concurrent.futures
import json
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from pathlib import Path
from unittest.mock import patch
from service.app import Store, Problem, make_server
TICKET={'event_id':'test-001','subject':'VPN connection fails','message':'VPN connection fails error 809'}
class StoreTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.store=Store(Path(self.temp.name)/'tickets.db')
    def tearDown(self):self.temp.cleanup()
    def test_retrieval_and_route(self):
        result=self.store.prepare(TICKET)
        self.assertEqual(result['sources'][0]['id'],'vpn')
        self.assertEqual(result['status'],'ready_to_send')
        self.assertEqual(result['provider'],'demo')
    def test_financial_review_and_replay(self):
        self.store.prepare({**TICKET,'subject':'Invoice refund','message':'Refund invoice payment'})
        review={'event_id':'test-001','decision':'approve'}
        self.assertEqual(self.store.review(review)['status'],'ready_to_send')
        self.store.review(review)
        self.assertEqual(len(self.store.events()),2)
        with self.assertRaises(Problem) as e:self.store.review({**review,'decision':'reject'})
        self.assertEqual(e.exception.status,409)
    def test_rejection(self):
        self.store.prepare({**TICKET,'subject':'urgent production outage'})
        self.assertEqual(self.store.review({'event_id':'test-001','decision':'reject'})['status'],'rejected')
    def test_duplicate(self):
        first=self.store.prepare(TICKET);second=self.store.prepare(TICKET)
        self.assertTrue(second['duplicate']);self.assertEqual(first['created_at'],second['created_at'])
        self.assertEqual(len(self.store.events()),1)
    def test_conflict(self):
        self.store.prepare(TICKET)
        with self.assertRaises(Problem) as e:self.store.prepare({**TICKET,'message':'changed'})
        self.assertEqual(e.exception.status,409)
    def test_concurrency(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
            results=list(pool.map(lambda _:self.store.prepare(TICKET),range(6)))
        self.assertEqual(sum(not r['duplicate'] for r in results),1)
        self.assertEqual(len(self.store.events()),1)
    def test_unknown(self):
        result=self.store.prepare({**TICKET,'subject':'xyz','message':'qwerty zxcv'})
        self.assertIn('weak_retrieval',result['review_reasons'])
    def test_model_failure(self):
        self.store.mode='ollama'
        with patch('service.app.urllib.request.urlopen',side_effect=OSError('offline')):
            result=self.store.prepare(TICKET)
        self.assertIn('model_unavailable',result['review_reasons'])
        self.assertEqual(result['status'],'pending_review')
    def test_generated_review(self):
        self.store.mode='ollama'
        with patch.object(self.store,'draft',return_value=('Check VPN.','ollama',None)):
            result=self.store.prepare(TICKET)
        self.assertIn('generated_draft',result['review_reasons'])
    def test_validation(self):
        for bad in [[],{}, {**TICKET,'message':None},{**TICKET,'event_id':'bad / id'},{**TICKET,'message':'x'*10001}]:
            with self.assertRaises(Problem):self.store.prepare(bad)
    def test_persistence(self):
        self.store.prepare(TICKET)
        self.assertTrue(Store(self.store.db).prepare(TICKET)['duplicate'])
class HTTPTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.server=make_server('127.0.0.1',0,Path(self.temp.name)/'db',api_token='i'*32,reviewer_token='r'*32,mode='demo')
        self.thread=threading.Thread(target=self.server.serve_forever,daemon=True);self.thread.start()
        self.base='http://127.0.0.1:'+str(self.server.server_port)
    def tearDown(self):
        self.server.shutdown();self.server.server_close();self.thread.join();self.temp.cleanup()
    def request(self,path,body=None,key=None):
        req=urllib.request.Request(self.base+path,data=json.dumps(body).encode() if body is not None else None,headers={'Content-Type':'application/json','X-API-Key':key or ''})
        try:
            with urllib.request.urlopen(req) as r:return r.status,json.load(r)
        except urllib.error.HTTPError as e:return e.code,json.load(e)
    def test_health_auth(self):
        self.assertEqual(self.request('/health')[0],200)
        self.assertEqual(self.request('/tickets/prepare',TICKET)[0],401)
        self.assertEqual(self.request('/tickets/prepare',TICKET,'i'*32)[0],200)
        self.assertEqual(self.request('/tickets',key='i'*32)[0],401)
        self.assertEqual(len(self.request('/tickets',key='r'*32)[1]['tickets']),1)
    def test_review_auth(self):
        body={'event_id':'absent','decision':'approve'}
        self.assertEqual(self.request('/tickets/review',body,'i'*32)[0],401)
        self.assertEqual(self.request('/tickets/review',body,'r'*32)[0],404)
    def test_validation_conflict(self):
        self.assertEqual(self.request('/tickets/prepare',{},'i'*32)[0],422)
        self.request('/tickets/prepare',TICKET,'i'*32)
        self.assertEqual(self.request('/tickets/prepare',{**TICKET,'message':'new'},'i'*32)[0],409)
if __name__=='__main__':unittest.main()
