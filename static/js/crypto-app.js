/**
 * 加密货币应用脚本
 */
document.addEventListener('DOMContentLoaded', function() {
    initApp();
    setupEventListeners();
    
    // 开始模拟价格更新
    fetchCryptoPrices();
    setInterval(fetchCryptoPrices, 10000); // 每10秒更新一次
});

/**
 * 初始化应用
 */
function initApp() {
    console.log('加密货币应用初始化');
    
    // 如果有欢迎横幅，设置延时关闭
    const welcomeBanner = document.querySelector('.welcome-banner');
    if (welcomeBanner) {
        setTimeout(() => {
            welcomeBanner.classList.add('closing');
            setTimeout(() => {
                welcomeBanner.style.display = 'none';
            }, 500);
        }, 5000);
    }
}

function setupEventListeners() {
    // 注意：所有页面跳转都使用HTML内联的onclick事件处理，避免在这里添加导航相关的监听器
    
    // 设置快速导航点击事件
    const quickNavItems = document.querySelectorAll('.quick-nav-item');
    if (quickNavItems.length > 0) {
        quickNavItems.forEach(item => {
            item.addEventListener('click', function() {
                const navText = this.querySelector('.nav-text').textContent;
                if (navText === '交易所') {
                    alert('交易所功能即将上线，敬请期待！');
                } else if (navText === '邀请好友') {
                    alert('邀请好友功能即将上线，敬请期待！');
                } else if (navText === '质押挖矿') {
                    alert('质押挖矿功能即将上线，敬请期待！');
                } else if (navText === 'AI助手') {
                    window.location.href = '/robot';
                } else {
                    alert('此功能正在开发中...');
                }
            });
        });
    }
    
    // 设置"查看更多"按钮点击事件
    const viewMoreBtn = document.querySelector('.view-more-btn');
    if (viewMoreBtn) {
        viewMoreBtn.addEventListener('click', function() {
            alert('更多加密货币数据正在加载中...');
        });
    }
}

function fetchCryptoPrices() {
    // 获取加密货币价格数据
    fetch('/api/crypto/prices')
        .then(response => response.json())
        .then(data => {
            if (data.code === 200) {
                updateCryptoPricesList(data.data);
            }
        })
        .catch(error => {
            console.error('获取加密货币价格失败:', error);
            // 如果API调用失败，使用模拟数据更新
            simulatePriceUpdates();
        });
}

function updateCryptoPricesList(cryptoData) {
    const cryptoList = document.querySelector('.crypto-list');
    if (!cryptoList) return;
    
    // 清空现有的列表
    cryptoList.innerHTML = '';
    
    // 添加新数据
    cryptoData.forEach(crypto => {
        const isPositive = crypto.change > 0;
        const changeClass = isPositive ? 'positive' : 'negative';
        const trendIcon = isPositive ? 'trend-up.svg' : 'trend-down.svg';
        
        const listItem = document.createElement('div');
        listItem.className = 'crypto-item';
        listItem.innerHTML = `
            <div class="crypto-info">
                <div class="crypto-name">${crypto.name}</div>
                <div class="crypto-symbol">${crypto.symbol}</div>
            </div>
            <div class="crypto-chart">
                <img src="/static/images/${trendIcon}" alt="趋势图">
            </div>
            <div class="crypto-price">
                <div class="price-value">$${crypto.price.toLocaleString()}</div>
                <div class="price-change ${changeClass}">${isPositive ? '+' : ''}${crypto.change}%</div>
            </div>
        `;
        
        cryptoList.appendChild(listItem);
    });
}

function simulatePriceUpdates() {
    // 模拟价格更新（当API不可用时）
    const cryptoItems = document.querySelectorAll('.crypto-item');
    
    cryptoItems.forEach(item => {
        const priceElement = item.querySelector('.price-value');
        const changeElement = item.querySelector('.price-change');
        const chartImage = item.querySelector('.crypto-chart img');
        
        if (priceElement && changeElement) {
            // 获取当前价格
            let currentPrice = parseFloat(priceElement.textContent.replace('$', '').replace(',', ''));
            
            // 随机生成价格变化（-2%到+2%之间）
            const changePercent = (Math.random() * 4 - 2).toFixed(2);
            const newPrice = currentPrice * (1 + changePercent / 100);
            
            // 更新价格显示
            priceElement.textContent = '$' + newPrice.toLocaleString(undefined, {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            });
            
            // 更新涨跌幅显示
            const isPositive = changePercent > 0;
            changeElement.textContent = `${isPositive ? '+' : ''}${changePercent}%`;
            changeElement.className = `price-change ${isPositive ? 'positive' : 'negative'}`;
            
            // 更新趋势图
            if (chartImage) {
                chartImage.src = `/static/images/${isPositive ? 'trend-up.svg' : 'trend-down.svg'}`;
            }
        }
    });
} 