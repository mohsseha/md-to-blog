Tags: Machine_Learning
Date: 2021-10-28			
			
# Even April Tags Can't Escape DL :) 

https://herohuyongtao.github.io/research/publications/deep-tag/teaser.png

I'm looking at this paper: 

https://arxiv.org/pdf/2105.13731.pdf

Nothing fancy but its the type of stuff that common ML tasks look like in the wild. Some interesting pointers: 
- This uses DL to identify the area that may have a tag. 
- Once we are sure that an area is of interest we "zoom" in and hand that over to the classic methods. 
- you are burning a lot more CPU but in exchange you get a substantial improvement in accuacy. 

Code seems to be at least partially available on [github](https://github.com/herohuyongtao/deeptag-pytorch)

