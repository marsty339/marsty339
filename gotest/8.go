function check_cluster_canary(){
    local KUBECTL="$1"
    local CLUSTER_NAME="$2"
    if [[ "$prdb_version" =~ ^v(3\.14) ]]; then
        log::info "====检查 ${CLUSTER_NAME} 集群是否有灰度发布的任务===="
        if $KUBECTL get manualgrayreleases.asm.alauda.io -A > /dev/null 2>&1 \
            || $KUBECTL get canarydeliveries.asm.alauda.io -A > /dev/null 2>&1; then
            log::err "检查不通过，${CLUSTER_NAME} 集群内有灰度发布的任务，请确认有无影响，有影响的话请联系产品经理，若无影响，请执行删除命令: kubectl delete canarydeliveries.asm.alauda.io  --all -A && kubectl delete manualgrayreleases.asm.alauda.io --all -A "
        else
            log::info "检查通过，${CLUSTER_NAME} 集群没有灰度发布任务"
        fi 
    fi
    if [[ "$prdb_version" =~ ^v(3\.12) ]]; then
        log::info "====检查 ${CLUSTER_NAME} 集群是否有灰度发布的任务===="
        if $KUBECTL get manualgrayreleases.asm.alauda.io -A > /dev/null 2>&1 \
            || $KUBECTL get canarydeliveries.asm.alauda.io -A > /dev/null 2>&1; then
            log::err "检查不通过，${CLUSTER_NAME} 集群内有灰度发布的任务，请确认有无影响，有影响的话请联系产品经理，若无影响，请执行命令: kubectl get canarydeliveries.asm.alauda.io -A --no-headers=true | awk '{print \"kubectl patch canarydeliveries.asm.alauda.io -n \"\$1,\$2\" --type='\''json'\'' -p='\''[{\\\"op\\\": \\\"replace\\\", \\\"path\\\": \\\"/spec/isavaliable\\\", \\\"value\\\": false}]'\''\"}' |bash && kubectl delete manualgrayreleases.asm.alauda.io --all -A "
        else 
            log::info "检查通过，${CLUSTER_NAME} 集群没有灰度发布任务"
        fi
 