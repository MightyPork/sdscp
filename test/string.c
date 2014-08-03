
#define INDEX "index.php"

#define MOO "(moo)"

task()
{
	http_get(198, 162, 11, 111, "localhost", MOO INDEX"?a=", sys[459], "&foo=", "bar");
}
