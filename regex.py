import unittest
import re


def get_time(status):
    match = re.match('.* ([0-9]+)h(([0-9]+)m)?.*', status)
    if match is None:
        return None
    hours, _, minutes = match.groups()
    return (int(hours) if hours is not None else 0,
            int(minutes) if minutes is not None else 0)


class TestRegex(unittest.TestCase):
    def test_regex(self):
        self.assertEqual(get_time('| 60% 3h55m OK'), (3, 55))
        self.assertEqual(get_time('| stracony sensor'), None)
        self.assertEqual(get_time('⚠ | 60% 8h30m'), (8, 30))
        self.assertEqual(get_time('⚠ | 67% 10h45m OK'), (10, 45))
        self.assertEqual(get_time('⚠ T:0J-56m | 12h -- 15,7 17,1 18,9'), (12, 0))
        self.assertEqual(get_time('⚠ T:150%-54m | 11h5m OK'), (11, 5))
        self.assertEqual(get_time('podawanie bolusa | 67% 7h5m'), (7, 5))
        self.assertEqual(get_time('sus | 12h + 16,1 14,6 14,5'), (12, 0))
        self.assertEqual(get_time('T:150%-1h29m | 60% 11h40m'), (11, 40))
        self.assertEqual(get_time('T:150%-1h47m | stracony sensor'), (None))
        self.assertEqual(get_time('T:150%-1h54m | 12h5m OK'), (12, 5))
        self.assertEqual(get_time('T:200%-58m | 6h35m OK'), (6, 35))
        self.assertEqual(get_time('wstrzymany | 67% 2h45m'), (2, 45))

if __name__ == '__main__':
    unittest.main()
