// Uncomment to get minimum footprint (suitable for 1-2 concurrent calls only)
#define PJ_CONFIG_MINIMAL_SIZE
// Uncomment to get maximum performance
//#define PJ_CONFIG_MAXIMUM_SPEED

#if !defined(_MSC_VER) && !defined(NO_FORCE_MSC_VER)
#define _MSC_VER 1400
#endif

#if !defined(_MSYS_VER)
#define _MSYS_VER 2
#endif

#define strerror_r(x, y, z) strerror_s(x, y,x)

#include <pj/config_site_sample.h>