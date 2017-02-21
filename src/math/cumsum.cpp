/*
 * DIPlib 3.0
 * This file contains the definition for the CumulativeSum function.
 *
 * (c)2017, Cris Luengo.
 * Based on original DIPlib code: (c)1995-2014, Delft University of Technology.
 */

#include "diplib.h"
#include "diplib/math.h"
#include "diplib/framework.h"
#include "diplib/overload.h"

namespace dip {

namespace {

template< typename TPI >
class CumSumFilter : public Framework::SeparableLineFilter {
      void Filter( Framework::SeparableLineFilterParameters const& params ) {
         TPI* in = static_cast< TPI* >( params.inBuffer.buffer );
         dip::uint length = params.inBuffer.length;
         dip::sint inStride = params.inBuffer.stride;
         TPI* out = static_cast< TPI* >( params.outBuffer.buffer );
         dip::sint outStride = params.outBuffer.stride;
         TPI sum = 0;
         for( dip::uint ii = 0; ii < length; ++ii ) {
            sum += *in;
            *out = sum;
            in += inStride;
            out += outStride;
         }
      }
};

} // namespace

void CumulativeSum(
      Image const& in,
      Image const& mask,
      Image& out,
      BooleanArray process
) {
   DIP_THROW_IF( !in.IsForged(), E::IMAGE_NOT_FORGED );
   DIP_THROW_IF( in.Dimensionality() < 1, E::DIMENSIONALITY_NOT_SUPPORTED );
   DataType dataType = DataType::SuggestFlex( in.DataType() );
   std::unique_ptr< Framework::SeparableLineFilter > lineFilter;
   DIP_OVL_NEW_FLEX( lineFilter, CumSumFilter, (), dataType );
   if( mask.IsForged() ) {
      mask.CheckIsMask( in.Sizes(), Option::AllowSingletonExpansion::DO_ALLOW, Option::ThrowException::DO_THROW );
      //out.ReForge( in, Option::AcceptDataTypeChange::DO_ALLOW );
      //out.CopyAt( mask );
      Convert( in, out, dataType );
      // TODO: set pixels not selected by mask to 0.
      Framework::Separable( out, out, dataType, out.DataType(),
                            process, { 0 }, {}, *lineFilter,
                            Framework::Separable_AsScalarImage );
   }
   Framework::Separable( in, out, dataType, out.DataType(),
                         process, { 0 }, {}, *lineFilter,
                         Framework::Separable_AsScalarImage );
}

} // namespace dip
