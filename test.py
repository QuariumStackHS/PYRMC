import PYRM.PYRM as PYR
aa=PYR.PYRM(mode="")
def main(*args):

    aa.Print("hello",*args)

aa.add_func(main, "hello", "info")
aa.post_init()