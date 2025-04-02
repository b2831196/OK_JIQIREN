/**
 * 检查是否有交易对添加到后端
 * @param {Function} callback - 如果有交易对，则调用此回调
 * @param {Function} errorCallback - 如果没有交易对或发生错误，调用此回调
 */
function checkTradingPairsBeforeStart(callback, errorCallback) {
    // 显示加载中提示
    if (typeof showLoading === 'function') {
        showLoading();
    }
    
    // 获取交易对列表
    fetch('/api/trading_pairs/list')
        .then(response => response.json())
        .then(data => {
            // 隐藏加载提示
            if (typeof hideLoading === 'function') {
                hideLoading();
            }
            
            if (data.code === 200 && Array.isArray(data.data)) {
                if (data.data.length === 0) {
                    // 没有交易对
                    console.error('没有添加交易对到后端，无法启动');
                    if (typeof errorCallback === 'function') {
                        errorCallback('请先添加至少一个交易对到后端才能启动');
                    }
                } else {
                    // 有交易对，可以继续
                    console.log(`检测到 ${data.data.length} 个交易对，可以启动`);
                    if (typeof callback === 'function') {
                        callback(data.data);
                    }
                }
            } else {
                // 请求失败
                console.error('获取交易对失败:', data.message || '未知错误');
                if (typeof errorCallback === 'function') {
                    errorCallback('获取交易对失败: ' + (data.message || '未知错误'));
                }
            }
        })
        .catch(error => {
            // 隐藏加载提示
            if (typeof hideLoading === 'function') {
                hideLoading();
            }
            
            console.error('网络错误，无法获取交易对列表:', error);
            if (typeof errorCallback === 'function') {
                errorCallback('网络错误，无法获取交易对列表');
            }
        });
}

/**
 * 修改后的saveStrategy函数，在启动前检查交易对
 * @param {boolean} shouldRunStrategy - 是否是运行策略（而不仅仅是保存）
 */
function saveStrategyWithCheck(shouldRunStrategy) {
    if (shouldRunStrategy) {
        // 如果是运行策略，先检查是否有交易对
        checkTradingPairsBeforeStart(
            // 有交易对，继续执行
            function(tradingPairs) {
                // 执行原始的saveStrategy函数
                if (typeof saveStrategy === 'function') {
                    saveStrategy(shouldRunStrategy);
                } else {
                    console.error('找不到saveStrategy函数');
                    showToast('错误', '系统错误：找不到保存策略函数', 'error');
                }
            },
            // 没有交易对或出错，显示错误信息
            function(errorMessage) {
                showToast('错误', errorMessage, 'error');
            }
        );
    } else {
        // 不是运行策略，直接执行
        if (typeof saveStrategy === 'function') {
            saveStrategy(shouldRunStrategy);
        } else {
            console.error('找不到saveStrategy函数');
            showToast('错误', '系统错误：找不到保存策略函数', 'error');
        }
    }
}

// 在页面加载时，为运行按钮添加新的事件处理器
document.addEventListener('DOMContentLoaded', function() {
    // 找到运行策略按钮
    const runButton = document.getElementById('run-strategy-btn');
    if (runButton) {
        // 移除原来的事件监听器（如果有的话）
        const oldButton = runButton.cloneNode(true);
        runButton.parentNode.replaceChild(oldButton, runButton);
        
        // 添加新的事件监听器
        oldButton.addEventListener('click', function() {
            saveStrategyWithCheck(true);
        });
        
        console.log('成功为运行按钮添加交易对检查逻辑');
    } else {
        console.error('找不到运行策略按钮');
    }
}); 