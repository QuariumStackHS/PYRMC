import PYRM.PYRM as PYR
aa=PYR.PYRM(mode="", can_exe_func_with_sysargv=True)
def main(*args):
    
    aa.Print("hello",*args)
def getpass():
    aa.Print("allo")
aa.add_func(getpass,"gt","info", False)
aa.add_func(main, "hello", "info", True)
aa.post_init()