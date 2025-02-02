#!/usr/bin/env python3
import argparse, sys, os, subprocess

SAMPLE1 = "sample1.txt"
SAMPLE2 = "sample2.txt"
SAMPLE3 = "sample3.txt"
SAMPLE4 = "sample4.txt"
SAMPLE_TEMP = "sample.txt.temp"
RESULT1 = "00000000004030000000000000203000"
RESULT2 = "00000000005030000000000000603000"
RESULT3 = "00000000005030000000000000603000"

class Test:
  def __init__(self):
    self.testNum = 1
  def test_pass(self, label):
    print("Test \033[1m{0}\033[0m \033[38;5;208m{1}\033[0m \033[32mOK\033[0m".format(self.testNum, label))
    self.testNum = self.testNum + 1
        
  def test_fail(self, label):
    print("Test \033[1m{0}\033[0m \033[38;5;208m{1}\033[0m \033[31mFAILED\033[0m".format(self.testNum, label))
    sys.exit(1)
    
def exec_process(args, useStd = True) -> int:
  if useStd:
    process = subprocess.Popen(args)
    stdout, stderr = process.communicate()
  else:
    process = subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    process.communicate()
  exit_code = process.wait()
  return exit_code

def read_file(file) -> str:
  with open(file) as f:
    content = f.read()
  return content

def getSample(file) -> str:
    p = os.path.join(os.getcwd(), "samples")
    return os.path.join(p, file)

def main(argv) -> int:
  parser = argparse.ArgumentParser()
  parser.add_argument("-f", "--file", help="Binary file.")
  parser.add_argument("-e", "--extra", action='store_true', help="Extra tests.")
  args = parser.parse_args()
  if args.file == None:
    print("Unspecified file name")
    sys.exit(1)
  if not os.path.exists(args.file):
    print("File {0} not found".format(args.file))
    sys.exit(1)
    
  t = Test()
  sample_dir = getSample(SAMPLE_TEMP)
  ret_code = exec_process([args.file, "-i", getSample(SAMPLE1), "-o", sample_dir, "-s", "6", "-l", "47"])
  if ret_code != 0:
    os.remove(sample_dir)
    t.test_fail("sample1 exec    ")
  t.test_pass("sample1 exec    ")

  result = read_file(sample_dir)
  if result != RESULT1:
    os.remove(sample_dir)
    t.test_fail("sample1 compare ")
  t.test_pass("sample1 compare ")

  ret_code = exec_process([args.file, "-i", getSample(SAMPLE2), "-o", sample_dir, "-l", "47"])
  if ret_code != 0:
    os.remove(sample_dir)
    t.test_fail("sample2 exec    ")
  t.test_pass("sample2 exec    ")

  result = read_file(sample_dir)
  if result != RESULT2:
    os.remove(sample_dir)
    t.test_fail("sample2 compare ")
  t.test_pass("sample2 compare ")

  ret_code = exec_process([args.file, "-i", getSample(SAMPLE3), "-o", sample_dir, "-s", "1"])
  if ret_code != 0:
    os.remove(sample_dir)
    t.test_fail("sample3 exec    ")
  t.test_pass("sample3 exec    ")

  if result != RESULT3:
    os.remove(sample_dir)
    t.test_fail("sample3 compare ")
  t.test_pass("sample3 compare ")

  if args.extra:
    ret_code = exec_process([args.file, "-i", getSample(SAMPLE4), "-o", sample_dir, "-s", "1"], False)
    if ret_code == 0:
      os.remove(sample_dir)
      t.test_fail("sample4 exec    ")
    t.test_pass("sample4 exec    ")

    ret_code = exec_process([args.file, "-i", getSample(SAMPLE3), "-o", sample_dir, "-p"], False)
    if ret_code != 0:
      os.remove(sample_dir)
      t.test_fail("print exec      ")
    t.test_pass("print exec      ")

    ret_code = exec_process([args.file, "-i", getSample(SAMPLE3), "-o", sample_dir, "-e"], False)
    if ret_code != 0:
      os.remove(sample_dir)
      t.test_fail("extract exec    ")
    t.test_pass("extract exec    ")

    ret_code = exec_process([args.file, "-0"], False)
    if ret_code == 0:
      t.test_fail("opt error      ")
    t.test_pass("opt error      ")

    ret_code = exec_process([args.file, "-o", "file_not_found"], False)
    os.remove("file_not_found")
    if ret_code == 0:
      t.test_fail("no in error    ")
    t.test_pass("no in error    ")

    ret_code = exec_process([args.file, "-i", getSample(SAMPLE3), "-s", "1"], False)
    if ret_code == 0:
      t.test_fail("no out error   ")
    t.test_pass("no out error   ")

    ret_code = exec_process([args.file], False)
    if ret_code == 0:
      t.test_fail("nofile error   ")
    t.test_pass("nofile error   ")

    ret_code = exec_process([args.file, "-i", "file_not_found"], False)
    if ret_code == 0:
      t.test_fail("file in error  ")
    t.test_pass("file in error  ")

    ret_code = exec_process([args.file, "-i", getSample(SAMPLE3), "-o", "/file_not_found"], False)
    if ret_code == 0:
      t.test_fail("file out error ")
    t.test_pass("file out error ")

    ret_code = exec_process([args.file, "-i", getSample(SAMPLE3), "-o", sample_dir], False)
    if ret_code == 0:
      os.remove(sample_dir)
      t.test_fail("even exec      ")
    t.test_pass("even exec      ")

    ret_code = exec_process([args.file, "-i", getSample(SAMPLE3), "-o", sample_dir, "-l", "az"], False)
    if ret_code == 0:
      t.test_fail("limit1 error   ")
    t.test_pass("limit1 error   ")

    ret_code = exec_process([args.file, "-i", getSample(SAMPLE3), "-o", sample_dir, "-l", "4294967295"], False)
    if ret_code == 0:
      t.test_fail("limit2 error   ")
    t.test_pass("limit2 error   ")

    ret_code = exec_process([args.file, "-i", getSample(SAMPLE3), "-o", sample_dir, "-l", "-1"], False)
    if ret_code == 0:
      t.test_fail("limit3 error   ")
    t.test_pass("limit3 error   ")

    ret_code = exec_process([args.file, "-i", getSample(SAMPLE3), "-o", sample_dir, "-s", "az"], False)
    if ret_code == 0:
      t.test_fail("start1 error   ")
    t.test_pass("start1 error   ")

    ret_code = exec_process([args.file, "-i", getSample(SAMPLE4), "-o", sample_dir, "-s", "6"], False)
    if ret_code == 0:
      t.test_fail("start2 error   ")
    t.test_pass("start2 error   ")

    ret_code = exec_process([args.file, "-i", getSample(SAMPLE4), "-o", sample_dir, "-s", "4294967295"], False)
    if ret_code == 0:
      t.test_fail("start3 error   ")
    t.test_pass("start3 error   ")

    ret_code = exec_process([args.file, "-i", getSample(SAMPLE4), "-o", sample_dir, "-s", "-1"], False)
    if ret_code == 0:
      t.test_fail("start4 error   ")
    t.test_pass("start4 error   ")

    ret_code = exec_process([args.file, "-i", getSample(SAMPLE1), "-o", sample_dir, "-s", "1", "-p"], False)
    if ret_code != 0:
      t.test_fail("start warning  ")
    t.test_pass("start warning  ")

  print("TEST \033[32mPASSED\033[0m")
  os.remove(sample_dir)
  return 0
  
if __name__ == '__main__':
  sys.exit(main(sys.argv[1:]))
