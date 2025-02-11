# User Stories

We have thus far created 3 user stories to guide our design of this software.


## User Story #1

"A user should be able to open the application, set their desired configuration details, and run the simulation."

Issues created from this story:
* **Python GUI** - Use PyQT to recreate the MatLab GUI we have within Python. This will serve as the frontend for our application.
* **Read Config from GUI** - Read what is entered into the application into a configuration file.
* **Send Config to Server** - Send the configuration file from the user application to the server so that it can call the FPIBG application

## User Story #2

"Once the configuration file has been sent off, the user should be able to switch to a secondary tab where they can view the visuals provided to summarize the simulation."

Issues created from this story:
* **Plot Tab** - The GUI needs a tab where the user can views plots of the simulation data.

## User Story #3

"Once the application is installed, the user should be able to run a series of tests to see whether or not the system will work on their machine."

Issues created from this story:
* **Verification Test #1 - Particle Quantity Benchmark** - Verify that the number of particles detected is the same as the number of particles loaded.  
Run n tests on a range between x and y particles.
* **Verification Test #2 - Particle Collision Density** - Verify that the number of collisions detected is the same as the number of collisions loaded.
* **Verification Test #3 - Cell Fraction Benchmark** - Verify that as you subdivide the space into boxes, the number of boxes created is what you would expect.
* **Verification Test #4 - Duplicates** - Particles can be on the boundary between cells, potentially causing those collisions to be counted twice. This test determines whether you get the number of collisions you would expect under this circumstance.
* **Performance Test #1 - Particle Quantity Benchmark** - Test how many particles you can have the machine run before its performance falls below an acceptable threshold.
* **Performance Test #2 - Particle Collision Density** - See how many collisions you can cause before the performance falls below an acceptable threshold.
* **Performance Test #3 - Cell Fraction Benchmark** - Test how the performance changers as you go from having one box with all the particles in it to many boxes with a few particles in each.