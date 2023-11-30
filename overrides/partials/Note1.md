# Notes for lecture 1&2

### string
we can initialize a string from a substring.
```C++
string(const char *cp);//C string
string(const char *cp, int len);//at most len chars ,\0 not included
string(const string& s2, int pos);//count from 0
string(const string& s2, int pos, int len);
string(int n,char c);//a string of n chars of c
```
The method for string:
```C++
int size()const; //same as length
char &at(int n);// like [],but check the range
void resize(int len,char c);//resize to length , padding with c
int find(const string &s, int pos = 0) const;//find substring s from pos , return string::npos if not found
```
Just some funcs I used for homework.For mor details, retrieve in this [blog](https://blog.csdn.net/qq_37954088/article/details/82286530)

### new and delete
!!! info
    the delete[] will not change the space it freed, but change the number of deconstructor it calls
### sort and stable_sort
```C++
#include <algorithm>
sort(first,last,cmp);
int cmp(const type& ,const type &);
```
sort will sort the elements in [first,last).
cmp will ensure every pair in the sorted array to return.


