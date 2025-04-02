document.addEventListener('DOMContentLoaded', function() {
    // 获取DOM元素
    const refreshBtn = document.querySelector('.refresh-btn');
    const menuItems = document.querySelectorAll('.menu-item');
    const userAvatar = document.querySelector('.user-avatar');
    
    // 随机生成数据的函数
    function generateRandomData() {
        const todayChats = Math.floor(Math.random() * 100);
        const totalChats = todayChats + Math.floor(Math.random() * 900);
        const robotCount = Math.floor(Math.random() * 10) + 1;
        const activeUsers = Math.floor(Math.random() * 50) + 1;
        
        return {
            todayChats,
            totalChats,
            robotCount,
            activeUsers
        };
    }
    
    // 更新数据显示
    function updateDashboard() {
        const data = generateRandomData();
        const metrics = document.querySelectorAll('.card-metric');
        
        metrics[0].textContent = data.todayChats;
        metrics[1].textContent = data.totalChats;
        metrics[2].textContent = data.robotCount;
        metrics[3].textContent = data.activeUsers;
    }
    
    // 刷新按钮点击事件
    refreshBtn.addEventListener('click', function() {
        updateDashboard();
        refreshBtn.classList.add('refreshing');
        
        setTimeout(() => {
            refreshBtn.classList.remove('refreshing');
        }, 500);
    });
    
    // 菜单项点击事件
    menuItems.forEach(item => {
        item.addEventListener('click', function() {
            // 移除所有active类
            menuItems.forEach(i => i.classList.remove('active'));
            // 给当前点击的项添加active类
            this.classList.add('active');
            
            // 显示相应的提示信息
            const menuText = this.querySelector('.menu-text').textContent;
            if (menuText !== '控制台') {
                alert(`${menuText}功能正在开发中，敬请期待！`);
            }
        });
    });
    
    // 初始化仪表盘数据
    updateDashboard();
}); 