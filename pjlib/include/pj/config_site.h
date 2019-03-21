//#define PJ_DLL 1
//#define PJ_EXPORTING 1
// #define PJ_EXPORT_DECL_SPECIFIER __declspec(dllexport)
// #define PJ_IMPORT_DECL_SPECIFIER __declspec(dllimport)

//#define PJ_EXPORT_SPECIFIER __declspec(dllexport)
//#define PJ_IMPORT_SPECIFIER __declspec(dllimport)

#define strerror_r(x,y,z) strerror_s(x, y,x)

#define PJ_CONFIG_MINIMAL_SIZE              1
#define PJ_OS_HAS_CHECK_STACK	            0
#define PJ_LOG_MAX_LEVEL		            0
#define PJ_ENABLE_EXTRA_CHECK	            0
#define PJ_HAS_ERROR_STRING		            0

#define PJ_ASSERT_RETURN                    1
#define PJ_FD_SETSIZE_SETABLE               1
/* Putting max handles to lower than 32 will make pj_fd_set_t size smaller
 * than native fdset_t and will trigger assertion on sock_select.c.
 */
#define PJ_IOQUEUE_MAX_HANDLES              32

#define PJ_CRC32_HAS_TABLES		            0
#define PJSIP_MAX_TSX_COUNT		            15
#define PJSIP_MAX_DIALOG_COUNT	            15
#define PJSIP_UDP_SO_SNDBUF_SIZE	        4000
#define PJSIP_UDP_SO_RCVBUF_SIZE	        4000
#define PJMEDIA_HAS_ALAW_ULAW_TABLE	        0


// Uncomment to get maximum performance
//#define PJ_CONFIG_MAXIMUM_SPEED           1
#define PJMEDIA_HAS_ILBC_CODEC              1
#define PJMEDIA_HAS_GSM_CODEC               1
#define PJMEDIA_HAS_G711_CODEC              1
#define PJMEDIA_HAS_GSM_CODEC               1
#define PJMEDIA_HAS_INTEL_IPP               0
#define PJMEDIA_HAS_INTEL_IPP_CODEC_G729    0
#define PJMEDIA_HAS_VIDEO                   0
#define PJMEDIA_HAS_SRTP                    0
#define PJMEDIA_HAS_G722_CODEC              0
#define PJMEDIA_HAS_SPEEX_CODEC             0
#define PJMEDIA_HAS_OPUS_CODEC              0
#define PJMEDIA_HAS_L16_CODEC               0
#define PJMEDIA_HAS_G722_CODEC              0
#define PJMEDIA_HAS_INTEL_IPP_CODEC_AMR     0
#define PJMEDIA_HAS_INTEL_IPP_CODEC_AMRWB   0
#define PJMEDIA_HAS_INTEL_IPP_CODEC_G723_1  0
#define PJMEDIA_HAS_INTEL_IPP_CODEC_G726    0
#define PJMEDIA_HAS_INTEL_IPP_CODEC_G728    0
#define PJMEDIA_HAS_INTEL_IPP_CODEC_G722_1  0
#define PJSIP_REGISTER_CLIENT_CHECK_CONTACT 0

