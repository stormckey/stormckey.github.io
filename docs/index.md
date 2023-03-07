<!-- ---
comments: true
--- -->

# Home

 Format testing now

An code seg to test:
```C
int main(){
    printf("Hello World");
}
```
```C++
#include <iostream>
using namespace std;
```
!!! note " my title"
    something
!!! note ""
    no title
??? note "my title"
    something
!!! info  "no inline"
    Now it suppports Note,Abstract,Info,Tip,Success,Question,Warining,Failure,Danger,Bug,Example,Quote
!!! info inline  "inline"
    somthing
[Subscribe to our newsletter](#){ .md-button }

[Subscribe to our newsletter](#){ .md-button .md-button--primary }

=== "C"

    ``` c
    #include <stdio.h>

    int main(void) {
      printf("Hello world!\n");
      return 0;
    }
    ```

=== "C++"

    ``` c++
    #include <iostream>

    int main(void) {
      std::cout << "Hello world!" << std::endl;
      return 0;
    }
    ```

<!-- ...

{{ read_excel('./Book1.xlsx',engine='openpyxl')}}

... -->
!!! note
    Search for emojis [here](https://squidfunk.github.io/mkdocs-material/reference/icons-emojis/)

:smile::sweat:

<figure markdown>
  ![Image title](https://dummyimage.com/600x400/){ width="300" }
  <figcaption>Image caption</figcaption>
</figure>
![Image title](https://dummyimage.com/600x400/){ loading=lazy }

- [x] Lorem ipsum dolor sit amet, consectetur adipiscing elit
- [ ] Vestibulum convallis sit amet nisi a tincidunt
    * [x] In hac habitasse platea dictumst
    * [x] In scelerisque nibh non dolor mollis congue sed et metus
    * [ ] Praesent sed risus massa
- [ ] Aenean pretium efficitur erat, donec pharetra, ligula non scelerisque

$$
\operatorname{ker} f=\{g\in G:f(g)=e_{H}\}{\mbox{.}}
$$
