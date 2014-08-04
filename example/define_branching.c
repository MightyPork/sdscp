#define DO_STUFF 1
#define BE_LAZY 0

// later...

func()
{
#ifdef DO_STUFF
    doing_stuff();
#else
    // NO STUFF!
#endif
}

main()
{

#ifndef BE_LAZY // if not lazy
	work_hard();
#endif

}
