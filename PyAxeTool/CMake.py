import sys, os, argparse
from PyAxe import AOS, ALog, AFile, AStr

ALog.enableFileSink(False)

def handle_sub_cmd_archetype_generate_lib(args):
    root_CMakeLists_content = """cmake_minimum_required(VERSION 3.10)
project($(FUBA) VERSION 0.0.1 LANGUAGES CXX)

option($(FUBA)_ENABLE_TESTING "Enable testing of the $(fuba) library." ON)

include("cmake/CMakeUtil.cmake")

set(CMAKE_CXX_STANDARD 11)

include_directories(${CMAKE_SOURCE_DIR}/include)

add_subdirectory(src)

if ($(FUBA)_ENABLE_TESTING)
  enable_testing()
  add_subdirectory(test)
endif()
"""
    src_CMakeLists_content = """file(GLOB SOURCE_FILES
  *.cc
  ${CMAKE_SOURCE_DIR}/include/$(fuba)/*.h
  ${CMAKE_CURRENT_SOURCE_DIR}/*.h)
  
add_library($(fuba) ${SOURCE_FILES})

install(TARGETS $(fuba) 
  ARCHIVE DESTINATION lib
  LIBRARY DESTINATION lib)
install(DIRECTORY ${CMAKE_SOURCE_DIR}/include/ DESTINATION include)
"""
    test_CMakeLists_content = """SetupGTest()

AddTest($(fuba)_test $(fuba))
"""
    cmake_CMakeUtil = """#================================================================
# 安装gtest 
#================================================================
macro(SetupGTest)
  include(ExternalProject)
  
  # 创建自定义目标buildgtest
  ExternalProject_Add(
    SetupGTest
    URL https://github.com/google/googletest/archive/release-1.10.0.zip
    PREFIX ${CMAKE_BINARY_DIR}/thirdparty/gtest
    CMAKE_ARGS -DCMAKE_INSTALL_PREFIX:PATH=${CMAKE_BINARY_DIR}/thirdparty/gtest -DBUILD_SHARED_LIBS=OFF
  )
  
  # 获取目标属性
  ExternalProject_Get_property(SetupGTest INSTALL_DIR)
  SET(GTEST_INCLUDE_DIR "${INSTALL_DIR}/include")
  SET(GTEST_LIB_DIR "${INSTALL_DIR}/lib")
endmacro(SetupGTest)

#================================================================
# 增加一个依赖gtest的测试用例
#================================================================
macro(AddTest name depend_libs)
  add_executable(${name} "${name}.cc")
  add_dependencies(${name} SetupGTest)
  target_include_directories(${name} PUBLIC ${GTEST_INCLUDE_DIR})
  target_link_directories(${name} PUBLIC ${GTEST_LIB_DIR})
  target_link_libraries(${name} pthread gtest gtest_main ${depend_libs})
  add_test(NAME ${name} COMMAND ${name})
endmacro(AddTest)
"""
    lib_h = """#pragma once

namespace $(fuba) {
    
int Sum(int a, int b);

}  // namespace $(fuba)
"""
    lib_cc = """#include "$(fuba)/$(fuba).h"

namespace $(fuba) {
    
int Sum(int a, int b) {
  return a + b;
}

}  // namespace $(fuba)
"""

    lib_test_cc = """#include "$(fuba)/$(fuba).h"

#include <iostream>

#include "gtest/gtest.h"

TEST($(fuba)_test, Sum) {
  EXPECT_TRUE($(fuba)::Sum(1, 2) == 3);
}
"""
    if args.libname is None:
        print('missing --libname=<LIBNAME>')
        sys.exit(1)
    print(args.libname)
    
    fu_ba_map = AStr.getFuBaMap(args.libname, '')
    AOS.makeDir(fu_ba_map['fuba'])
    with AOS.ChangeDir(fu_ba_map['fuba']):
        AOS.makeDir(os.path.join('include', fu_ba_map['fuba']))
        AOS.makeDir('src')
        AOS.makeDir('test')
        AOS.makeDir('cmake')

        # CMakeLists相关
        AFile.write('CMakeLists.txt', AStr.format(root_CMakeLists_content, '$(', ')', **fu_ba_map), 'utf8')
        AFile.write(os.path.join('src', 'CMakeLists.txt'), AStr.format(src_CMakeLists_content, '$(', ')', **fu_ba_map), 'utf8')
        AFile.write(os.path.join('test', 'CMakeLists.txt'), AStr.format(test_CMakeLists_content, '$(', ')', **fu_ba_map), 'utf8')
        AFile.write(os.path.join('cmake', 'CMakeUtil.cmake'), cmake_CMakeUtil, 'utf8')
        
        # 源码相关
        AFile.write(os.path.join('include', fu_ba_map['fuba'], fu_ba_map['fuba']+'.h'), AStr.format(lib_h, '$(', ')', **fu_ba_map), 'utf8')
        AFile.write(os.path.join('src', fu_ba_map['fuba']+'.cc'), AStr.format(lib_cc, '$(', ')', **fu_ba_map), 'utf8')
        AFile.write(os.path.join('test', fu_ba_map['fuba']+'_test.cc'), AStr.format(lib_test_cc, '$(', ')', **fu_ba_map), 'utf8')
    
def handle_sub_cmd_archetype_generate(args):
    funcs = {
        'lib': handle_sub_cmd_archetype_generate_lib,
    }
    funcs[args.archetype](args)

def parse_args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='sub_cmd')
    subparser = subparsers.add_parser('archetype:generate', help='通过模板创建项目')
    subparser.add_argument('archetype', choices=['lib'], help='模板名称')
    subparser.add_argument('--libname', help='库名（仅当archetype为lib时有效）')

    return parser.parse_args()

g_args = parse_args()

def main():
    funcs = {
        'archetype:generate': handle_sub_cmd_archetype_generate,
    }
    funcs[g_args.sub_cmd](g_args)
    
if __name__ == '__main__':
    main()