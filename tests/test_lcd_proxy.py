import unittest
from lcd_ui import LCDProxy

class TestLCDProxy(unittest.TestCase):
    def test_init(self):
        p = LCDProxy()
        self.assertEqual(p.lcd, [bytearray(' '*16,encoding='utf-8'),bytearray(' '*16,encoding='utf-8')])

    def test_str_repr(self):
        p = LCDProxy(chars=5, rows=1, init_char='A')
        intended_output ='A A A A A' 
        self.assertEqual(str(p),intended_output)

    def test_write(self):
        p = LCDProxy(chars=5, rows=1)
        intended_output = 'A B C D E'
        p.write('A',[0,0])
        p.write('B',[0,1])
        p.write('C',[0,2])
        p.write('D',[0,3])
        p.write('E',[0,4])
        self.assertEqual(str(p),intended_output)

    def test_write_word(self):
        p = LCDProxy(chars=5,rows=1)
        intended_output = 'A B C D E'
        p.write_word('ABCDE',[0,0])
        self.assertEqual(str(p),intended_output)


if __name__ == '__main__':
    unittest.main()