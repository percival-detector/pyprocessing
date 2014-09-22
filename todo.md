Tasks and work todo
===================

 1. Develop a script which will generate a small set of test files to run processing on
  * Use numpy to generate appropriate datasets
  * Store datasets in HDF5 format
  * A file for each detector size: P2M, P13M
  * Different datasets for SAMPLE and RESET frames
  * Different datasets with varying noise levels
 2. Implement functions to carry out the 9 steps of processing required
  * Note that some functions have alternatives - which also need to be implemented.
  * Implementation in a fashion so that the individual functions can be enabled/disabled and replaced by alternative implementations
 3. Measure the performance of the implemented functions
  * See for instance ipython %time or %timeit
  
