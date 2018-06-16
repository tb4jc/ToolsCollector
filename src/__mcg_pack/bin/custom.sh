#! /bin/bash
# SCRIPT_DIR = where jenkins.inc is located (help functions to log)
# COMPONENT_REPOSITORY = repository for components
# DELIVERY_ROOT = where delivery should be placed
set -u

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source $SCRIPT_DIR/jenkins.inc


#--
# 
function log()
{
	print_info "[MCGPack] ${1}"
}

#-
#- $1 target (mcg|mcg2|nrtos4)
#- $2 component name (as in versions.inc)
#- $3 file pattern of dlu files
#- $4 destination, relative to delivery path
# uses:
#	PACK_ROOT
#	DELIVERY_ROOT
#	DELIVERY_ROOT_NRTOS
function copy_dlu()
{
	local TARGET=${1}
    local TARGET_FALLBACK
    if [ "${TARGET}" = "mcg" ]; then
        TARGET_FALLBACK=ccuc
    elif [ "${TARGET}" = "mcg2" ]; then
        TARGET_FALLBACK=nrtos
    else
        TARGET_FALLBACK=nrtos4
	fi
	
	local COMPONENT_NAME=${2}
	local FILE_PATTERN=${3}
	local SUBDIR=${4}

	local DEST=${DELIVERY_ROOT}/${SUBDIR}
	mkdir -p ${DEST}
	check_errs $? "[MCGPack] Could not create dir ${DEST}"

	set +u
	if [ -z "${MCG_VERSION}" ]; then
		MCG_VERSION=""
	fi
	set -u
	if [ "${COMPONENT_NAME}" == "mcg_firmware" ] && [ "${MCG_VERSION}" == "0.0.0.0" ]; then
		# special handling for mcg_firmware:
		# if the environment variable MCG_VERSION exists and is et to "0.0.0.0" we want to package
		# a trunk build and therefore ignore the version file entry for mcg_firmware
		local COMPONENT_VERSION=${MCG_VERSION}
		log "packaging ${COMPONENT_NAME} TRUNK VERSION ${COMPONENT_VERSION}"
	else
		local COMPONENT_VERSION=$( grep ^${COMPONENT_NAME}/ ${PACK_ROOT}/versions.inc | awk -F/ '{print $2}' )
		log "packaging ${COMPONENT_NAME} ${COMPONENT_VERSION}"
	fi

    if [ -d ${COMPONENT_REPOSITORY}/${COMPONENT_NAME}/${COMPONENT_VERSION}/dlu/${TARGET} ]; then
        cp -r ${COMPONENT_REPOSITORY}/${COMPONENT_NAME}/${COMPONENT_VERSION}/dlu/${TARGET}/${FILE_PATTERN} ${DEST}
    else
        cp -r ${COMPONENT_REPOSITORY}/${COMPONENT_NAME}/${COMPONENT_VERSION}/dlu/${TARGET_FALLBACK}/${FILE_PATTERN} ${DEST}
    fi
	check_errs $? "[MCGPack] Could not copy ${COMPONENT_NAME} ${COMPONENT_VERSION} ${FILE_PATTERN}"
}


#-
#- TARGET independent component having files directly under version directory
#- $1 component name (as in versions.inc)
#- $2 file pattern of dlu files
#- $3 destination, relative to delivery path
# uses:
#	PACK_ROOT
function copy_comp()
{
	local COMPONENT_NAME=${1}
	local FILE_PATTERN=${2}
	local SUBDIR=${3}

	local DEST=${DELIVERY_ROOT}/${SUBDIR}
	mkdir -p ${DEST}
	check_errs $? "[MCGPack] Could not create dir ${DEST}"

	local COMPONENT_VERSION=($( grep ^${COMPONENT_NAME}/ ${PACK_ROOT}/versions.inc | awk -F/ '{print $2}' ))
	log "packaging ${COMPONENT_NAME} ${COMPONENT_VERSION}"

	cp -r ${COMPONENT_REPOSITORY}/${COMPONENT_NAME}/${COMPONENT_VERSION}/${FILE_PATTERN} ${DEST}
	check_errs $? "[MCGPack] Could not copy ${COMPONENT_NAME} ${COMPONENT_VERSION} ${FILE_PATTERN}"
}


#-
# uses:
#	TARGET (mcg|mcg2|nrtos4)
#	PACK_ROOT
function pack()
{
	local TARGET=${1}

	# 01_os_base ###############################################
	log "pack OS BASE"
	copy_dlu ${TARGET} nrtos_prod_base "0000-rts_nrt?ppc.dl2" 01_os_base
	if [ "${TARGET}" = "nrtos4" ]; then
		copy_dlu ${TARGET} nrtos_prod_base "*.manifest" 01_os_base
	fi

	log "pack BASE"
    copy_dlu ${TARGET} cm       "*.dl2" 01_os_base
	copy_dlu ${TARGET} qt-build "*.dl2" 01_os_base


	# 02_middleware ###############################################
	log "pack MIDDLEWARE"
	copy_dlu ${TARGET} tds-com "*.dl2" 02_middleware
	copy_dlu ${TARGET} tds-tcl "*.dl2" 02_middleware
	
	if [ "${TARGET}" = "nrtos4" ]; then
		copy_dlu ${TARGET} tssp-ip "*.dl2" 02_middleware
	else
		copy_dlu ${TARGET} tssp-ip "dlu_new/*.dl2" 02_middleware
	fi
	copy_dlu ${TARGET} vrs-ip  "*.dl2" 02_middleware


	# 03_mcg_firmware ###############################################
	if [ "${TARGET}" = "mcg" ] || [ "${TARGET}" = "mcg2" ] || [ "${TARGET}" = "nrtos4" ]
    then 
        log "pack MCG FIRMWARE"
        copy_dlu ${TARGET} mcg_firmware "0000-mcg_*.dl2" 03_mcg_firmware

        # 04_cfg ###############################################
        log "pack CONFIGURATION"
        copy_dlu ${TARGET} mcg_config "*" 04_cfg

        local MCG_CONFIG_BIN_VERSION=($( grep ^mcg_config_bin/ ${PACK_ROOT}/versions.inc | awk -F/ '{print $2}' ))
        if [ ${MCG_CONFIG_BIN_VERSION} = "1.0.0.0" ]
        then
            copy_comp mcg_config_bin "*" 04_cfg/01_bin
        else
            copy_comp mcg_config_bin "output/*" 04_cfg/01_bin
        fi
    fi
}

#------------------------------------------------------------------------------
#  main
#------------------------------------------------------------------------------

log "--------------------------------------------------------------------------"
log "Packaging "${MCG_TARGET^^}
log "--------------------------------------------------------------------------"
pack ${MCG_TARGET}
