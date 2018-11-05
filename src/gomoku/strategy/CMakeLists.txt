add_executable(strategy main.cpp nodehandle.cpp strategy.cpp)
target_link_libraries(strategy ${catkin_LIBRARIES} )
add_dependencies(strategy ${${PROJECT_NAME}_EXPORTED_TARGETS} ${catkin_EXPORTED_TARGETS})

#find_package(OpenCV)
#include_directories($ {} OpenCV_INCLUDE_DIRS)
#target_link_libraries(aim ${OpenCV_LIBRARIES})
