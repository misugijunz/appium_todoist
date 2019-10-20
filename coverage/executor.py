import argparse

parser = argparse.ArgumentParser(description='Process test with options.')
parser.add_argument('--token', required=True)
parser.add_argument('--module',
                    help='Function module to be tested eg: Project',
                    default='project')
parser.add_argument('--email',
                    help='email to log in to app', required=True)
parser.add_argument('--password',
                    help='email to log in to app', required=True)
parsed_obj = parser.parse_args()

if __name__ == '__main__':
    unittest.main()