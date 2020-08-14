Tags:	Machine_Learning
	    Software_engineering
Date: 2020-06-29

# Making KFP Simple Again! 

While using KFP as a production back-end @ irobot my team hit a number of pain points for my team. They needed to: 

- run locally and be productive
- run on a cluster and not fight tooling, specifically KFP itself.  

Here is an approach that I found to be very productive: 

- Use light weight component pipeline composition.
- Standardized components (using [dockerfiles](http://www.docker.com)) to simplify debugging in different contexts.

An example of this type of system can be seen here:

http://GitHub.com/mohsseha/simple-kfp 

kfp.png

