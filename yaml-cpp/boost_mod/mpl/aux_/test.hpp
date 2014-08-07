
#ifndef BOOST_MPL_AUX_TEST_HPP_INCLUDED
#define BOOST_MPL_AUX_TEST_HPP_INCLUDED

// Copyright Aleksey Gurtovoy 2002-2004
//
// Distributed under the Boost Software License, Version 1.0. 
// (See accompanying file LICENSE_1_0.txt or copy at 
// http://www.boost.org/LICENSE_1_0.txt)
//
// See http://www.boost.org/libs/mpl for documentation.

// $Id: test.hpp 49267 2008-10-11 06:19:02Z agurtovoy $
// $Date: 2008-10-10 23:19:02 -0700 (Fri, 10 Oct 2008) $
// $Revision: 49267 $

#include "yaml-cpp/boost_mod/mpl/aux_/test/test_case.hpp"
#include "yaml-cpp/boost_mod/mpl/aux_/test/data.hpp"
#include "yaml-cpp/boost_mod/mpl/aux_/test/assert.hpp"
#include "yaml-cpp/boost_mod/detail/lightweight_test.hpp"

#include "yaml-cpp/boost_mod/type_traits/is_same.hpp"

int main()
{
    return boost::report_errors();
}

using namespace boost;
using namespace mpl;

#endif // BOOST_MPL_AUX_TEST_HPP_INCLUDED