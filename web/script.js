// 导航菜单功能
document.addEventListener('DOMContentLoaded', function() {
    const hamburger = document.getElementById('hamburger');
    const navMenu = document.getElementById('nav-menu');
    const navLinks = document.querySelectorAll('.nav-link');
    const sections = document.querySelectorAll('.section');

    // 移动端菜单切换
    hamburger.addEventListener('click', function() {
        navMenu.classList.toggle('active');
    });

    // 导航链接点击事件
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            // 移除所有active类
            navLinks.forEach(l => l.classList.remove('active'));
            sections.forEach(s => s.classList.remove('active'));
            
            // 添加active类到当前链接
            this.classList.add('active');
            
            // 显示对应的section
            const targetId = this.getAttribute('href').substring(1);
            const targetSection = document.getElementById(targetId);
            if (targetSection) {
                targetSection.classList.add('active');
            }
            
            // 关闭移动端菜单
            navMenu.classList.remove('active');
        });
    });

    // 初始化图表
    initCharts();
    
    // 初始化数据更新
    initDataUpdates();
    
    // 初始化实时数据
    initRealTimeData();
});

// 图表初始化
function initCharts() {
    // 收益曲线图
    const profitCtx = document.getElementById('profitChart');
    if (profitCtx) {
        new Chart(profitCtx, {
            type: 'line',
            data: {
                labels: ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月'],
                datasets: [{
                    label: '收益率',
                    data: [2.5, 5.2, 8.1, 12.3, 10.8, 15.6, 18.2, 16.9, 22.4],
                    borderColor: '#667eea',
                    backgroundColor: 'rgba(102, 126, 234, 0.1)',
                    borderWidth: 2,
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: function(value) {
                                return value + '%';
                            }
                        }
                    }
                }
            }
        });
    }

    // 股票mini图表
    const stockCharts = ['stockChart1', 'stockChart2', 'stockChart3'];
    const stockData = [
        [12.1, 12.3, 12.2, 12.5, 12.4, 12.6, 12.45],
        [1650, 1665, 1680, 1670, 1675, 1682, 1678.9],
        [238, 235, 233, 236, 234, 235.2, 234.56]
    ];

    stockCharts.forEach((chartId, index) => {
        const ctx = document.getElementById(chartId);
        if (ctx) {
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: ['09:30', '10:30', '11:30', '13:00', '14:00', '15:00'],
                    datasets: [{
                        data: stockData[index],
                        borderColor: index === 2 ? '#e74c3c' : '#27ae60',
                        backgroundColor: 'transparent',
                        borderWidth: 2,
                        pointRadius: 0,
                        tension: 0.4
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false }
                    },
                    scales: {
                        x: { display: false },
                        y: { display: false }
                    }
                }
            });
        }
    });
}

// 数据更新功能
function initDataUpdates() {
    const updateButtons = document.querySelectorAll('.update-btn');
    
    updateButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            const originalText = this.textContent;
            this.textContent = '更新中...';
            this.disabled = true;
            
            // 模拟更新过程
            setTimeout(() => {
                this.textContent = '更新完成';
                
                // 更新时间
                const timeSpan = this.parentElement.querySelector('.update-time');
                if (timeSpan) {
                    const now = new Date();
                    timeSpan.textContent = `最后更新: ${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-${String(now.getDate()).padStart(2, '0')} ${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}:${String(now.getSeconds()).padStart(2, '0')}`;
                }
                
                setTimeout(() => {
                    this.textContent = originalText;
                    this.disabled = false;
                }, 1000);
            }, 2000);
        });
    });
}

// 实时数据更新
function initRealTimeData() {
    // 模拟实时更新股价
    setInterval(() => {
        updateStockPrices();
        updateTradingRecords();
        updateStockStats();
    }, 5000);
    
    // 模拟市场指数更新
    setInterval(() => {
        updateMarketIndices();
    }, 10000);
    
    // 更新热点股票状态
    setInterval(() => {
        updateHotStocks();
    }, 15000);
}

// 更新热点股票
function updateHotStocks() {
    const hotStocks = document.querySelectorAll('.hot-stock');
    hotStocks.forEach(stock => {
        const random = Math.random();
        if (random < 0.3) {
            stock.className = 'hot-stock up';
            if (!stock.textContent.includes('↑')) {
                stock.textContent = stock.textContent.replace(' ↓', '') + ' ↑';
            }
        } else if (random < 0.6) {
            stock.className = 'hot-stock neutral';
            stock.textContent = stock.textContent.replace(' ↑', '').replace(' ↓', '');
        } else {
            if (Math.random() < 0.1) { // 10%概率变为下跌
                stock.className = 'hot-stock neutral'; // 保持中性显示
                stock.textContent = stock.textContent.replace(' ↑', '').replace(' ↓', '');
            }
        }
    });
}

// 更新股价
function updateStockPrices() {
    const stockPrices = document.querySelectorAll('.stock-price .current');
    const changes = document.querySelectorAll('.stock-price .change');
    
    stockPrices.forEach((priceElement, index) => {
        const currentPrice = parseFloat(priceElement.textContent);
        const changePercent = (Math.random() - 0.5) * 0.04; // -2% to +2%
        const newPrice = currentPrice * (1 + changePercent);
        const changeValue = newPrice - currentPrice;
        
        priceElement.textContent = newPrice.toFixed(2);
        
        if (changes[index]) {
            const changeText = `${changeValue >= 0 ? '+' : ''}${changeValue.toFixed(2)} (${changePercent >= 0 ? '+' : ''}${(changePercent * 100).toFixed(2)}%)`;
            changes[index].textContent = changeText;
            changes[index].className = `change ${changePercent >= 0 ? 'positive' : 'negative'}`;
        }
    });
}

// 更新市场指数
function updateMarketIndices() {
    const indices = document.querySelectorAll('.index');
    
    indices.forEach(indexElement => {
        const priceElement = indexElement.querySelector('.price');
        const changeElement = indexElement.querySelector('.change');
        
        if (priceElement && changeElement) {
            const currentPrice = parseFloat(priceElement.textContent.replace(',', ''));
            const changePercent = (Math.random() - 0.5) * 0.02; // -1% to +1%
            const newPrice = currentPrice * (1 + changePercent);
            
            priceElement.textContent = newPrice.toLocaleString('zh-CN', { 
                minimumFractionDigits: 2, 
                maximumFractionDigits: 2 
            });
            
            changeElement.textContent = `${changePercent >= 0 ? '+' : ''}${(changePercent * 100).toFixed(2)}%`;
            changeElement.className = `change ${changePercent >= 0 ? 'positive' : 'negative'}`;
        }
    });
}

// 更新交易记录
function updateTradingRecords() {
    const tableBody = document.getElementById('tradingTableBody');
    if (!tableBody) return;
    
    const now = new Date();
    const timeString = `${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}:${String(now.getSeconds()).padStart(2, '0')}`;
    
    const basePrices = [44.06, 44.07, 44.08, 44.09, 44.10, 44.11];
    const volumes = [1, 2, 5, 8, 13, 18, 24, 38, 76];
    const priceChanges = [-0.03, -0.02, -0.01, 0.00, 0.01, 0.02, 0.03];
    const natures = ['买盘', '卖盘'];
    
    const randomPrice = basePrices[Math.floor(Math.random() * basePrices.length)];
    const randomVolume = volumes[Math.floor(Math.random() * volumes.length)];
    const randomChange = priceChanges[Math.floor(Math.random() * priceChanges.length)];
    const randomNature = natures[Math.floor(Math.random() * natures.length)];
    const amount = (randomPrice * randomVolume * 100).toLocaleString();
    
    const changeClass = randomChange > 0 ? 'positive' : randomChange < 0 ? 'negative' : 'neutral';
    const natureClass = randomNature === '买盘' ? 'sell' : 'buy';
    
    const newRow = document.createElement('tr');
    newRow.innerHTML = `
        <td class="time">${timeString}</td>
        <td class="price">${randomPrice.toFixed(2)}</td>
        <td class="change ${changeClass}">${randomChange.toFixed(2)}</td>
        <td class="volume">${randomVolume}</td>
        <td class="amount">${amount}</td>
        <td class="nature ${natureClass}">${randomNature}</td>
    `;
    
    tableBody.insertBefore(newRow, tableBody.firstChild);
    
    // 保持最多20条记录
    const rows = tableBody.querySelectorAll('tr');
    if (rows.length > 20) {
        tableBody.removeChild(rows[rows.length - 1]);
    }
}

// 搜索功能
function initSearch() {
    const searchInput = document.querySelector('.search-input');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            // 这里可以实现搜索逻辑
            console.log('搜索:', searchTerm);
        });
    }
}

// 表单提交处理
function handleFormSubmissions() {
    // 策略创建
    const strategyBtns = document.querySelectorAll('.strategy-actions .btn');
    strategyBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const action = this.textContent;
            showNotification(`${action}功能开发中...`);
        });
    });
    
    // 论坛发帖
    const forumBtn = document.querySelector('.forum-controls .btn-primary');
    if (forumBtn) {
        forumBtn.addEventListener('click', function() {
            showNotification('发表主题功能开发中...');
        });
    }
}

// 通知系统
function showNotification(message) {
    // 创建通知元素
    const notification = document.createElement('div');
    notification.className = 'notification';
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 100px;
        right: 20px;
        background: #667eea;
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 5px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        z-index: 1001;
        opacity: 0;
        transform: translateX(100px);
        transition: all 0.3s ease;
    `;
    
    document.body.appendChild(notification);
    
    // 显示动画
    setTimeout(() => {
        notification.style.opacity = '1';
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    // 自动隐藏
    setTimeout(() => {
        notification.style.opacity = '0';
        notification.style.transform = 'translateX(100px)';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

// 数据格式化工具
function formatNumber(num, decimals = 2) {
    return num.toLocaleString('zh-CN', {
        minimumFractionDigits: decimals,
        maximumFractionDigits: decimals
    });
}

function formatCurrency(num) {
    return '¥' + formatNumber(num, 0);
}

function formatPercent(num) {
    return (num >= 0 ? '+' : '') + formatNumber(num, 2) + '%';
}

// 初始化所有功能
document.addEventListener('DOMContentLoaded', function() {
    initSearch();
    handleFormSubmissions();
    initStockInteractions();
    initBacktestModal();
    initHomePageInteractions();
    
    // 添加加载动画
    const cards = document.querySelectorAll('.card, .strategy-card, .news-card, .post-card');
    cards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
    });
});

// 股票页面交互功能
function initStockInteractions() {
    // 时间滑块交互
    const timeSlider = document.querySelector('.time-slider');
    const sliderHandle = document.querySelector('.slider-handle');
    const timeRange = document.querySelector('.time-range');
    
    if (timeSlider && sliderHandle) {
        let isDragging = false;
        
        timeSlider.addEventListener('mousedown', function(e) {
            isDragging = true;
            updateSliderPosition(e);
        });
        
        document.addEventListener('mousemove', function(e) {
            if (isDragging) {
                updateSliderPosition(e);
            }
        });
        
        document.addEventListener('mouseup', function() {
            isDragging = false;
        });
        
        function updateSliderPosition(e) {
            const rect = timeSlider.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const percentage = Math.max(0, Math.min(100, (x / rect.width) * 100));
            
            sliderHandle.style.left = percentage + '%';
            
            // 更新时间范围显示
            const totalMinutes = 360; // 6小时
            const currentMinutes = (percentage / 100) * totalMinutes + 570; // 从9:30开始
            const hours = Math.floor(currentMinutes / 60);
            const mins = Math.floor(currentMinutes % 60);
            const endMins = mins + 1;
            
            if (timeRange) {
                timeRange.textContent = `${hours}:${String(mins).padStart(2, '0')} - ${hours}:${String(endMins).padStart(2, '0')}`;
            }
        }
    }
    
    // 时间导航按钮
    const timeNavButtons = document.querySelectorAll('.time-nav');
    timeNavButtons.forEach(button => {
        button.addEventListener('click', function() {
            const isLeft = this.textContent === '◀';
            const currentLeft = parseInt(sliderHandle.style.left) || 45;
            const newLeft = isLeft ? Math.max(0, currentLeft - 5) : Math.min(100, currentLeft + 5);
            sliderHandle.style.left = newLeft + '%';
            
            // 触发位置更新
            const rect = timeSlider.getBoundingClientRect();
            const fakeEvent = {
                clientX: rect.left + (newLeft / 100) * rect.width
            };
            updateSliderPosition(fakeEvent);
        });
    });
    
    // 添加到自选股功能
    const addToFavoritesBtn = document.querySelector('.add-to-favorites');
    if (addToFavoritesBtn) {
        addToFavoritesBtn.addEventListener('click', function() {
            if (this.textContent.includes('加入')) {
                this.textContent = '✓ 已加入自选股';
                this.style.background = '#27ae60';
                this.style.color = 'white';
                this.style.borderColor = '#27ae60';
                showNotification('已加入自选股');
            } else {
                this.textContent = '+ 加入自选股';
                this.style.background = '#f8f9fa';
                this.style.color = '#333';
                this.style.borderColor = '#ddd';
                showNotification('已移出自选股');
            }
        });
    }
    
    // 侧边栏菜单交互
    const menuSections = document.querySelectorAll('.menu-section h4');
    menuSections.forEach(section => {
        section.addEventListener('click', function() {
            const submenu = this.nextElementSibling;
            if (submenu) {
                const isExpanded = submenu.style.display !== 'none';
                submenu.style.display = isExpanded ? 'none' : 'block';
                this.textContent = this.textContent.replace(
                    isExpanded ? '▼' : '▶', 
                    isExpanded ? '▶' : '▼'
                );
            }
        });
    });
    
    // 子菜单项点击
    const subMenuItems = document.querySelectorAll('.sub-menu li');
    subMenuItems.forEach(item => {
        item.addEventListener('click', function() {
            subMenuItems.forEach(i => i.classList.remove('active'));
            this.classList.add('active');
            
            // 模拟切换不同视图
            const viewName = this.textContent;
            showNotification(`切换到${viewName}视图`);
        });
    });
    
    // 清空访问记录
    const clearHistory = document.querySelector('.clear-history');
    if (clearHistory) {
        clearHistory.addEventListener('click', function() {
            const recentStocks = document.querySelector('.recent-stocks');
            if (recentStocks) {
                recentStocks.innerHTML = '<div style="text-align: center; color: #999; padding: 1rem;">暂无访问记录</div>';
                showNotification('访问记录已清空');
            }
        });
    }
    
    // 热点股票点击
    const hotStocks = document.querySelectorAll('.hot-stock');
    hotStocks.forEach(stock => {
        stock.addEventListener('click', function() {
            const stockName = this.textContent.replace(' ↑', '').replace(' ↓', '');
            showNotification(`正在加载${stockName}行情数据...`);
            
            // 模拟加载新股票数据
            setTimeout(() => {
                updateStockData(stockName);
            }, 1000);
        });
    });
    
    // 股票搜索功能
    const stockSearch = document.getElementById('stockSearch');
    if (stockSearch) {
        stockSearch.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                const searchValue = this.value.trim();
                if (searchValue) {
                    showNotification(`正在搜索${searchValue}...`);
                    setTimeout(() => {
                        updateStockData(searchValue);
                    }, 1000);
                }
            }
        });
    }
}

// 模拟更新股票数据
function updateStockData(stockName) {
    const stockTitle = document.querySelector('.stock-title h2');
    const currentPrice = document.querySelector('.current-price');
    const priceChange = document.querySelector('.price-change');
    
    if (stockTitle) stockTitle.textContent = stockName;
    
    // 生成随机股价数据
    const randomPrice = (Math.random() * 100 + 10).toFixed(2);
    const randomChange = ((Math.random() - 0.5) * 5).toFixed(2);
    const randomPercent = ((randomChange / randomPrice) * 100).toFixed(2);
    
    if (currentPrice) {
        currentPrice.textContent = randomPrice + (randomChange >= 0 ? ' ↑' : ' ↓');
        currentPrice.className = `current-price ${randomChange >= 0 ? 'positive' : 'negative'}`;
    }
    
    if (priceChange) {
        priceChange.textContent = `${randomChange >= 0 ? '+' : ''}${randomChange}  ${randomChange >= 0 ? '+' : ''}${randomPercent}%`;
        priceChange.className = `price-change ${randomChange >= 0 ? 'positive' : 'negative'}`;
    }
    
    showNotification(`${stockName} 数据更新完成`);
}

// 更新股票统计数据
function updateStockStats() {
    const currentPrice = document.querySelector('.current-price');
    if (!currentPrice) return;
    
    const priceText = currentPrice.textContent.replace(' ↑', '').replace(' ↓', '');
    const price = parseFloat(priceText);
    const changePercent = (Math.random() - 0.5) * 0.02; // -1% to +1%
    const newPrice = price * (1 + changePercent);
    const changeValue = newPrice - price;
    
    currentPrice.textContent = newPrice.toFixed(2) + (changeValue >= 0 ? ' ↑' : ' ↓');
    currentPrice.className = `current-price ${changeValue >= 0 ? 'positive' : 'negative'}`;
    
    const priceChange = document.querySelector('.price-change');
    if (priceChange) {
        priceChange.textContent = `${changeValue >= 0 ? '+' : ''}${changeValue.toFixed(2)}  ${changeValue >= 0 ? '+' : ''}${(changePercent * 100).toFixed(2)}%`;
        priceChange.className = `price-change ${changeValue >= 0 ? 'positive' : 'negative'}`;
    }
    
    // 更新时间戳
    const updateTime = document.querySelector('.update-time');
    if (updateTime) {
        const now = new Date();
        updateTime.textContent = `${String(now.getMonth() + 1).padStart(2, '0')}-${String(now.getDate()).padStart(2, '0')} ${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}:${String(now.getSeconds()).padStart(2, '0')}`;
    }
}

// 响应式图表调整
window.addEventListener('resize', function() {
    // 这里可以添加图表响应式调整逻辑
    Chart.helpers.each(Chart.instances, function(instance) {
        instance.resize();
    });
});

// 滚动优化
let ticking = false;

function updateScrollPosition() {
    const scrolled = window.pageYOffset;
    const header = document.querySelector('.header');
    
    if (scrolled > 50) {
        header.style.background = 'rgba(102, 126, 234, 0.95)';
        header.style.backdropFilter = 'blur(10px)';
    } else {
        header.style.background = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
        header.style.backdropFilter = 'none';
    }
    
    ticking = false;
}

window.addEventListener('scroll', function() {
    if (!ticking) {
        requestAnimationFrame(updateScrollPosition);
        ticking = true;
    }
});

// 键盘快捷键
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + K 快速搜索
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        const searchInput = document.querySelector('.search-input');
        if (searchInput) {
            searchInput.focus();
        }
    }
    
    // ESC 关闭移动端菜单
    if (e.key === 'Escape') {
        const navMenu = document.getElementById('nav-menu');
        navMenu.classList.remove('active');
    }
});

// 性能监控
function logPerformance() {
    if ('performance' in window) {
        window.addEventListener('load', function() {
            setTimeout(function() {
                const perfData = performance.timing;
                const networkLatency = perfData.responseStart - perfData.navigationStart;
                const pageLoadTime = perfData.loadEventStart - perfData.navigationStart;
                
                console.log('页面性能数据:');
                console.log('网络延迟:', networkLatency + 'ms');
                console.log('页面加载时间:', pageLoadTime + 'ms');
            }, 0);
        });
    }
}

logPerformance();

// 回测详情模态对话框功能
function initBacktestModal() {
    const modal = document.getElementById('backtestModal');
    const closeBtn = document.querySelector('.close');
    const detailButtons = document.querySelectorAll('.backtest-detail-btn');
    
    // 打开模态对话框
    detailButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            const strategyName = this.dataset.strategy;
            const strategyReturn = this.dataset.return;
            const strategyAuthor = this.dataset.author;
            const strategyParams = this.dataset.params;
            
            openBacktestModal(strategyName, strategyReturn, strategyAuthor, strategyParams);
        });
    });
    
    // 关闭模态对话框
    closeBtn.addEventListener('click', closeBacktestModal);
    
    // 点击背景关闭
    window.addEventListener('click', function(event) {
        if (event.target === modal) {
            closeBacktestModal();
        }
    });
    
    // ESC键关闭
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape' && modal.classList.contains('active')) {
            closeBacktestModal();
        }
    });
    
    // 时间周期选择器
    const periodButtons = document.querySelectorAll('.period-btn');
    periodButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            periodButtons.forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            
            const period = this.dataset.period;
            updateBacktestChart(period);
        });
    });
}

// 打开回测详情模态对话框
function openBacktestModal(strategyName, strategyReturn, strategyAuthor, strategyParams) {
    const modal = document.getElementById('backtestModal');
    
    // 更新基本信息
    document.getElementById('strategyName').textContent = strategyName;
    document.getElementById('strategyAuthor').textContent = strategyAuthor;
    document.getElementById('strategyParams').textContent = strategyParams;
    
    // 根据策略生成随机但合理的回测数据
    const returnValue = parseFloat(strategyReturn);
    const isProfit = returnValue > 0;
    
    // 更新统计数据
    document.getElementById('totalReturn').textContent = `${returnValue >= 0 ? '+' : ''}${returnValue.toFixed(2)}%`;
    document.getElementById('totalReturn').className = `stat-value ${isProfit ? 'positive' : 'negative'}`;
    
    const annualReturn = (returnValue * 2.1).toFixed(2);
    document.getElementById('annualReturn').textContent = `${annualReturn >= 0 ? '+' : ''}${annualReturn}%`;
    document.getElementById('annualReturn').className = `stat-value ${annualReturn >= 0 ? 'positive' : 'negative'}`;
    
    const maxDrawdown = -(Math.abs(returnValue) * 0.3 + Math.random() * 5).toFixed(2);
    document.getElementById('maxDrawdown').textContent = `${maxDrawdown}%`;
    
    const sharpeRatio = isProfit ? (1.2 + Math.random() * 0.8).toFixed(2) : (0.3 + Math.random() * 0.5).toFixed(2);
    document.getElementById('sharpeRatio').textContent = sharpeRatio;
    
    const profitTrades = Math.floor(100 + Math.random() * 200);
    const lossTrades = Math.floor(50 + Math.random() * 150);
    const winRate = ((profitTrades / (profitTrades + lossTrades)) * 100).toFixed(2);
    
    document.getElementById('profitTrades').textContent = profitTrades.toString();
    document.getElementById('lossTrades').textContent = lossTrades.toString();
    document.getElementById('winRate').textContent = `${winRate}%`;
    
    const avgHoldingDays = (5 + Math.random() * 20).toFixed(1);
    document.getElementById('avgHoldingDays').textContent = `${avgHoldingDays}天`;
    
    // 显示模态对话框
    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
    
    // 延迟渲染图表确保容器可见
    setTimeout(() => {
        initBacktestChart();
        generateTradingLog(strategyName);
    }, 100);
}

// 关闭回测详情模态对话框
function closeBacktestModal() {
    const modal = document.getElementById('backtestModal');
    modal.classList.remove('active');
    document.body.style.overflow = 'auto';
}

// 初始化回测图表
let backtestChart = null;

function initBacktestChart() {
    const ctx = document.getElementById('backtestChart');
    if (!ctx) return;
    
    // 如果图表已存在则先销毁
    if (backtestChart) {
        backtestChart.destroy();
    }
    
    // 生成回测数据
    const dates = [];
    const strategyReturns = [];
    const benchmarkReturns = [];
    
    const startDate = new Date('2015-01-01');
    const endDate = new Date('2015-06-01');
    const daysDiff = Math.floor((endDate - startDate) / (1000 * 60 * 60 * 24));
    
    let strategyValue = 100;
    let benchmarkValue = 100;
    
    for (let i = 0; i <= daysDiff; i += 5) { // 每5天一个数据点
        const currentDate = new Date(startDate.getTime() + i * 24 * 60 * 60 * 1000);
        dates.push(currentDate.toLocaleDateString('zh-CN', { month: '2-digit', day: '2-digit' }));
        
        // 策略收益模拟（有一定波动但整体向上）
        const strategyChange = (Math.random() - 0.45) * 2; // 略偏正的随机波动
        strategyValue *= (1 + strategyChange / 100);
        strategyReturns.push(((strategyValue - 100) / 100) * 100);
        
        // 基准收益模拟（较平稳）
        const benchmarkChange = (Math.random() - 0.5) * 1;
        benchmarkValue *= (1 + benchmarkChange / 100);
        benchmarkReturns.push(((benchmarkValue - 100) / 100) * 100);
    }
    
    backtestChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: dates,
            datasets: [{
                label: '策略收益',
                data: strategyReturns,
                borderColor: '#3498db',
                backgroundColor: 'rgba(52, 152, 219, 0.1)',
                borderWidth: 2,
                fill: true,
                tension: 0.4
            }, {
                label: '基准收益',
                data: benchmarkReturns,
                borderColor: '#e74c3c',
                backgroundColor: 'rgba(231, 76, 60, 0.1)',
                borderWidth: 2,
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
                },
                tooltip: {
                    mode: 'index',
                    intersect: false,
                    callbacks: {
                        label: function(context) {
                            return context.dataset.label + ': ' + context.parsed.y.toFixed(2) + '%';
                        }
                    }
                }
            },
            interaction: {
                mode: 'nearest',
                axis: 'x',
                intersect: false
            },
            scales: {
                x: {
                    display: true,
                    title: {
                        display: true,
                        text: '日期'
                    }
                },
                y: {
                    display: true,
                    title: {
                        display: true,
                        text: '收益率 (%)'
                    },
                    ticks: {
                        callback: function(value) {
                            return value.toFixed(1) + '%';
                        }
                    }
                }
            }
        }
    });
}

// 更新回测图表（根据时间周期）
function updateBacktestChart(period) {
    if (!backtestChart) return;
    
    // 根据不同周期调整数据点数量
    let dataPoints;
    switch(period) {
        case '1m':
            dataPoints = 6;
            break;
        case '3m':
            dataPoints = 18;
            break;
        case '6m':
            dataPoints = 36;
            break;
        default: // 'all'
            dataPoints = backtestChart.data.labels.length;
            break;
    }
    
    // 截取数据
    const originalData = backtestChart.data;
    backtestChart.data.labels = originalData.labels.slice(-dataPoints);
    backtestChart.data.datasets.forEach(dataset => {
        dataset.data = dataset.data.slice(-dataPoints);
    });
    
    backtestChart.update();
    
    showNotification(`已切换到${period === 'all' ? '全部' : period}时间周期`);
}

// 生成交易记录
function generateTradingLog(strategyName) {
    const tableBody = document.getElementById('tradingLogBody');
    if (!tableBody) return;
    
    // 清空现有数据
    tableBody.innerHTML = '';
    
    // 模拟交易记录数据
    const stocks = ['000001', '600519', '002594', '000002', '600036', '000858'];
    const trades = [];
    
    // 生成20条交易记录
    for (let i = 0; i < 20; i++) {
        const isRecent = i < 10;
        const date = isRecent 
            ? new Date(2015, 4, 30 - i * 2).toLocaleDateString('zh-CN')  // 近期交易
            : new Date(2015, Math.floor(Math.random() * 4), Math.floor(Math.random() * 28) + 1).toLocaleDateString('zh-CN');
        
        const stock = stocks[Math.floor(Math.random() * stocks.length)];
        const isSell = Math.random() > 0.5;
        const price = (10 + Math.random() * 200).toFixed(2);
        const quantity = Math.floor(100 + Math.random() * 2000);
        const commission = (parseFloat(price) * quantity * 0.0005).toFixed(2);
        
        let profit = '-';
        if (isSell) {
            const profitValue = (Math.random() - 0.3) * 2000; // 略偏正的利润
            profit = profitValue.toFixed(2);
        }
        
        trades.push({
            date,
            stock,
            action: isSell ? '卖出' : '买入',
            price,
            quantity,
            commission,
            profit
        });
    }
    
    // 排序（最新的在前）
    trades.sort((a, b) => new Date(b.date) - new Date(a.date));
    
    // 填充表格
    trades.forEach(trade => {
        const row = document.createElement('tr');
        const profitClass = trade.profit !== '-' ? (parseFloat(trade.profit) >= 0 ? 'positive' : 'negative') : '';
        const profitDisplay = trade.profit !== '-' ? (parseFloat(trade.profit) >= 0 ? '+' : '') + trade.profit : '-';
        
        row.innerHTML = `
            <td>${trade.date}</td>
            <td>${trade.stock}</td>
            <td class="trade-${trade.action === '买入' ? 'buy' : 'sell'}">${trade.action}</td>
            <td>${trade.price}</td>
            <td>${trade.quantity}</td>
            <td>${trade.commission}</td>
            <td class="${profitClass}">${profitDisplay}</td>
        `;
        
        tableBody.appendChild(row);
    });
}

// 首页交互功能
function initHomePageInteractions() {
    // 更多链接点击
    const moreLinks = document.querySelectorAll('.more-link');
    moreLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            
            // 切换到对应页面
            const navLinks = document.querySelectorAll('.nav-link');
            const sections = document.querySelectorAll('.section');
            
            navLinks.forEach(l => l.classList.remove('active'));
            sections.forEach(s => s.classList.remove('active'));
            
            const targetNavLink = document.querySelector(`a[href="#${targetId}"]`);
            const targetSection = document.getElementById(targetId);
            
            if (targetNavLink && targetSection) {
                targetNavLink.classList.add('active');
                targetSection.classList.add('active');
            }
        });
    });
    
    // 策略卡片操作
    const strategyButtons = document.querySelectorAll('.strategy-actions .btn');
    strategyButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            const action = this.textContent;
            const strategyCard = this.closest('.strategy-card');
            const strategyName = strategyCard.querySelector('h3').textContent;
            
            if (action.includes('详情')) {
                showNotification(`正在查看 ${strategyName} 详情...`);
            } else if (action.includes('克隆')) {
                this.textContent = '已克隆';
                this.style.background = '#27ae60';
                showNotification(`成功克隆策略: ${strategyName}`);
                
                setTimeout(() => {
                    this.textContent = '克隆策略';
                    this.style.background = '';
                }, 3000);
            }
        });
    });
    
    // 新闻点击
    const newsItems = document.querySelectorAll('.news-card, .news-item');
    newsItems.forEach(item => {
        item.addEventListener('click', function() {
            const title = this.querySelector('h3, h4').textContent;
            showNotification(`正在阅读: ${title}`);
        });
    });
    
    // 帖子点击
    const postCards = document.querySelectorAll('.post-card');
    postCards.forEach(post => {
        post.addEventListener('click', function() {
            const title = this.querySelector('h3').textContent;
            showNotification(`正在查看帖子: ${title}`);
        });
    });
    
    // 首页数据动态更新
    setInterval(() => {
        updateHomePageStats();
    }, 30000); // 30秒更新一次
}

// 更新首页统计数据
function updateHomePageStats() {
    // 更新用户数
    const userStat = document.querySelector('.stat-number');
    if (userStat && userStat.textContent.includes('10,000')) {
        const currentNum = parseInt(userStat.textContent.replace(/[^\d]/g, ''));
        const newNum = currentNum + Math.floor(Math.random() * 50);
        userStat.textContent = newNum.toLocaleString() + '+';
    }
    
    // 更新平均年化收益
    const returnStats = document.querySelectorAll('.stat-number');
    returnStats.forEach(stat => {
        if (stat.textContent.includes('%')) {
            const currentReturn = parseFloat(stat.textContent);
            const change = (Math.random() - 0.5) * 0.2; // ±0.1%的变化
            const newReturn = Math.max(10, Math.min(20, currentReturn + change));
            stat.textContent = newReturn.toFixed(1) + '%';
        }
    });
    
    // 更新阅读量
    const viewCounts = document.querySelectorAll('.news-views');
    viewCounts.forEach(view => {
        if (view.textContent.includes('阅读')) {
            const text = view.textContent;
            if (text.includes('万')) {
                const num = parseFloat(text);
                const newNum = (num + Math.random() * 0.1).toFixed(1);
                view.textContent = `🔥 ${newNum}万阅读`;
            } else {
                const num = parseInt(text.replace(/[^\d]/g, ''));
                const newNum = num + Math.floor(Math.random() * 100);
                view.textContent = `${newNum}阅读`;
            }
        }
    });
    
    // 更新帖子统计
    const postStats = document.querySelectorAll('.post-stats .stat');
    postStats.forEach(stat => {
        if (stat.textContent.includes('浏览')) {
            const text = stat.textContent;
            if (text.includes('k')) {
                const num = parseFloat(text);
                const newNum = (num + Math.random() * 0.1).toFixed(1);
                stat.textContent = `🔥 ${newNum}k浏览`;
            }
        } else if (stat.textContent.includes('回复')) {
            const num = parseInt(stat.textContent.replace(/[^\d]/g, ''));
            if (Math.random() < 0.3) { // 30%概率增加回复
                stat.textContent = `💬 ${num + 1}回复`;
            }
        } else if (stat.textContent.includes('点赞')) {
            const num = parseInt(stat.textContent.replace(/[^\d]/g, ''));
            if (Math.random() < 0.2) { // 20%概率增加点赞
                stat.textContent = `👍 ${num + Math.floor(Math.random() * 3)}点赞`;
            }
        }
    });
}

// ==================== 悬浮智能助手功能 ====================

// 初始化悬浮助手
document.addEventListener('DOMContentLoaded', function() {
    initChatFloat();
});

function initChatFloat() {
    const chatFloatBtn = document.getElementById('chatFloatBtn');
    const chatPopup = document.getElementById('chatPopup');
    const closeBtn = document.getElementById('closeBtn');
    const minimizeBtn = document.getElementById('minimizeBtn');
    const chatPopupInput = document.getElementById('chatPopupInput');
    const chatPopupSend = document.getElementById('chatPopupSend');
    const chatPopupMessages = document.getElementById('chatPopupMessages');
    const quickBtns = document.querySelectorAll('.quick-btn');
    const openChatLink = document.getElementById('openChatLink');

    // 悬浮按钮点击事件
    chatFloatBtn.addEventListener('click', function() {
        toggleChatPopup();
    });

    // 首页"开始对话"链接点击事件
    if (openChatLink) {
        openChatLink.addEventListener('click', function(e) {
            e.preventDefault();
            showChatPopup();
        });
    }

    // 关闭按钮
    closeBtn.addEventListener('click', function() {
        hideChatPopup();
    });

    // 最小化按钮
    minimizeBtn.addEventListener('click', function() {
        hideChatPopup();
    });

    // 发送消息
    chatPopupSend.addEventListener('click', function() {
        sendMessage();
    });

    // 输入框回车发送
    chatPopupInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    // 快捷按钮点击
    quickBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const query = this.getAttribute('data-query');
            chatPopupInput.value = query;
            sendMessage();
        });
    });

    // 点击外部关闭弹窗
    document.addEventListener('click', function(e) {
        if (!chatPopup.contains(e.target) && !chatFloatBtn.contains(e.target)) {
            if (chatPopup.classList.contains('show')) {
                hideChatPopup();
            }
        }
    });
}

function toggleChatPopup() {
    const chatPopup = document.getElementById('chatPopup');
    if (chatPopup.classList.contains('show')) {
        hideChatPopup();
    } else {
        showChatPopup();
    }
}

function showChatPopup() {
    const chatPopup = document.getElementById('chatPopup');
    chatPopup.classList.add('show');
    
    // 聚焦输入框
    setTimeout(() => {
        const input = document.getElementById('chatPopupInput');
        if (input) input.focus();
    }, 100);
}

function hideChatPopup() {
    const chatPopup = document.getElementById('chatPopup');
    chatPopup.classList.remove('show');
}

function sendMessage() {
    const input = document.getElementById('chatPopupInput');
    const messagesContainer = document.getElementById('chatPopupMessages');
    const message = input.value.trim();
    
    if (!message) return;

    // 添加用户消息
    addMessage('user', message);
    
    // 清空输入框
    input.value = '';
    
    // 显示"正在输入"指示
    addTypingIndicator();
    
    // 模拟AI回复
    setTimeout(() => {
        removeTypingIndicator();
        const response = generateAIResponse(message);
        addMessage('bot', response);
    }, 1500);
}

function addMessage(type, content) {
    const messagesContainer = document.getElementById('chatPopupMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}-message`;
    
    const now = new Date();
    const timeStr = now.getHours().toString().padStart(2, '0') + ':' + 
                   now.getMinutes().toString().padStart(2, '0');
    
    if (type === 'user') {
        messageDiv.innerHTML = `
            <div class="message-avatar">👤</div>
            <div class="message-content">
                <div class="message-text">${content}</div>
                <div class="message-time">${timeStr}</div>
            </div>
        `;
    } else {
        messageDiv.innerHTML = `
            <div class="message-avatar">🤖</div>
            <div class="message-content">
                <div class="message-text">${content}</div>
                <div class="message-time">${timeStr}</div>
            </div>
        `;
    }
    
    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function addTypingIndicator() {
    const messagesContainer = document.getElementById('chatPopupMessages');
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message bot-message typing-indicator';
    typingDiv.innerHTML = `
        <div class="message-avatar">🤖</div>
        <div class="message-content">
            <div class="message-text">
                正在思考中<span class="dots">...</span>
            </div>
        </div>
    `;
    
    messagesContainer.appendChild(typingDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
    
    // 添加点点动画
    const dots = typingDiv.querySelector('.dots');
    let dotCount = 0;
    const dotInterval = setInterval(() => {
        dotCount = (dotCount + 1) % 4;
        dots.textContent = '.'.repeat(dotCount);
    }, 500);
    
    typingDiv.dotInterval = dotInterval;
}

function removeTypingIndicator() {
    const messagesContainer = document.getElementById('chatPopupMessages');
    const typingIndicator = messagesContainer.querySelector('.typing-indicator');
    if (typingIndicator) {
        if (typingIndicator.dotInterval) {
            clearInterval(typingIndicator.dotInterval);
        }
        typingIndicator.remove();
    }
}

function generateAIResponse(userMessage) {
    const message = userMessage.toLowerCase();
    
    // 简单的关键词匹配回复
    if (message.includes('平安银行') || message.includes('000001')) {
        return `
            平安银行（000001.SZ）实时分析：<br><br>
            📊 当前价格：12.45元 <span style="color: #e74c3c;">↑ +2.35%</span><br>
            📈 成交量：3.2万手<br>
            💰 换手率：0.89%<br><br>
            💡 技术分析：股价突破5日均线，短期趋势转强，MACD金叉形成，建议关注。
        `;
    } else if (message.includes('贵州茅台') || message.includes('600519')) {
        return `
            贵州茅台（600519.SH）分析报告：<br><br>
            📊 当前价格：1,680.50元 <span style="color: #27ae60;">↑ +1.28%</span><br>
            📈 成交量：1.8万手<br>
            💰 市值：2.1万亿<br><br>
            💡 投资建议：白酒龙头，长期价值投资标的，当前估值合理。
        `;
    } else if (message.includes('涨停') || message.includes('涨停股票')) {
        return `
            📈 今日涨停股票概览：<br><br>
            🔥 <strong>新能源板块</strong>：<br>
            • 比亚迪 (+10.02%)<br>
            • 宁德时代 (+10.01%)<br>
            • 理想汽车 (+9.98%)<br><br>
            🔥 <strong>AI概念</strong>：<br>
            • 科大讯飞 (+10.00%)<br>
            • 海康威视 (+9.99%)<br><br>
            💡 建议关注板块轮动机会，注意风险控制。
        `;
    } else if (message.includes('大盘') || message.includes('走势')) {
        return `
            📊 大盘走势分析：<br><br>
            🔹 上证指数：3,812.51 <span style="color: #27ae60;">↑ +1.24%</span><br>
            🔹 深证成指：12,590.56 <span style="color: #27ae60;">↑ +3.89%</span><br>
            🔹 创业板指：2,456.78 <span style="color: #27ae60;">↑ +2.35%</span><br><br>
            💡 技术面：三大指数集体上涨，科技股领涨，市场情绪向好，建议关注热点板块机会。
        `;
    } else if (message.includes('北向资金') || message.includes('资金流向')) {
        return `
            💰 北向资金流向分析：<br><br>
            📈 今日净流入：+126.8亿元<br>
            🎯 主要流入板块：<br>
            • 金融：+45.2亿<br>
            • 消费：+38.9亿<br>
            • 科技：+42.7亿<br><br>
            💡 北向资金持续流入，显示外资对A股信心增强，建议关注外资偏好的优质标的。
        `;
    } else if (message.includes('科技股') || message.includes('科技板块')) {
        return `
            🔬 科技板块今日表现：<br><br>
            📊 板块涨幅：+4.23%<br>
            🔥 领涨个股：<br>
            • 华为概念：+6.78%<br>
            • 芯片半导体：+5.92%<br>
            • 人工智能：+5.45%<br><br>
            💡 科技股受政策利好推动，建议关注龙头企业，注意估值风险。
        `;
    } else if (message.includes('财务') || message.includes('财报')) {
        return `
            📋 财务数据查询功能：<br><br>
            我可以帮您分析：<br>
            📊 营收增长率<br>
            📈 净利润变化<br>
            💰 ROE/ROA指标<br>
            📉 负债率水平<br>
            💵 现金流状况<br><br>
            请告诉我具体要查询哪只股票的财务数据？
        `;
    } else if (message.includes('推荐') || message.includes('股票推荐')) {
        return `
            ⭐ 优质股票推荐（仅供参考）：<br><br>
            🏆 <strong>价值投资</strong>：<br>
            • 贵州茅台：白酒龙头，长期价值<br>
            • 中国平安：金融巨头，估值合理<br><br>
            🚀 <strong>成长投资</strong>：<br>
            • 宁德时代：新能源龙头<br>
            • 迈瑞医疗：医疗器械领军<br><br>
            ⚠️ 投资有风险，建议结合自身情况做决策。
        `;
    } else if (message.includes('创建') && (message.includes('策略') || message.includes('双均线') || message.includes('rsi') || message.includes('macd'))) {
        return generateStrategyCreationResponse(message);
    } else if (message.includes('分析') && (message.includes('策略') || message.includes('优缺点') || message.includes('优点') || message.includes('缺点'))) {
        return generateStrategyAnalysisResponse(message);
    } else {
        return `
            您好！我是QuanTrade智能助手，我可以帮您：<br><br>
            📈 查询个股信息（如：平安银行股价多少？）<br>
            📊 分析技术指标（如：贵州茅台技术分析）<br>
            💰 了解资金流向（如：北向资金情况）<br>
            🔍 市场热点解析（如：今日涨停股票）<br>
            🔧 创建量化策略（如：创建一个双均线策略）<br>
            🔍 分析策略优缺点（如：分析RSI策略的优缺点）<br><br>
            请尝试问我具体的股票、市场或策略问题！
        `;
    }
}

// 策略创建回复生成
function generateStrategyCreationResponse(message) {
    if (message.includes('双均线') || message.includes('均线')) {
        return `
            🔧 <strong>双均线交叉策略创建</strong><br><br>
            
            <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 10px 0;">
                <h4>📋 策略概述</h4>
                基于短期均线与长期均线的交叉信号进行买卖决策的经典量化策略。<br><br>
                
                <h4>⚙️ 策略参数</h4>
                • <strong>短期均线</strong>：5日移动平均线（MA5）<br>
                • <strong>长期均线</strong>：20日移动平均线（MA20）<br>
                • <strong>买入信号</strong>：MA5上穿MA20（金叉）<br>
                • <strong>卖出信号</strong>：MA5下穿MA20（死叉）<br><br>
                
                <h4>💻 Python代码框架</h4>
                <div style="background: #2c3e50; color: #ecf0f1; padding: 10px; border-radius: 4px; font-family: monospace; font-size: 12px;">
def dual_ma_strategy(data):<br>
&nbsp;&nbsp;&nbsp;&nbsp;# 计算移动平均线<br>
&nbsp;&nbsp;&nbsp;&nbsp;data['MA5'] = data['close'].rolling(5).mean()<br>
&nbsp;&nbsp;&nbsp;&nbsp;data['MA20'] = data['close'].rolling(20).mean()<br>
&nbsp;&nbsp;&nbsp;&nbsp;<br>
&nbsp;&nbsp;&nbsp;&nbsp;# 生成交易信号<br>
&nbsp;&nbsp;&nbsp;&nbsp;data['signal'] = 0<br>
&nbsp;&nbsp;&nbsp;&nbsp;data.loc[data['MA5'] > data['MA20'], 'signal'] = 1  # 买入<br>
&nbsp;&nbsp;&nbsp;&nbsp;data.loc[data['MA5'] < data['MA20'], 'signal'] = -1  # 卖出<br>
&nbsp;&nbsp;&nbsp;&nbsp;<br>
&nbsp;&nbsp;&nbsp;&nbsp;return data
                </div>
            </div>
            
            ✅ <strong>策略已生成！</strong>您可以在策略研究页面进一步优化参数。
        `;
    } else if (message.includes('rsi')) {
        return `
            🔧 <strong>RSI反转策略创建</strong><br><br>
            
            <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 10px 0;">
                <h4>📋 策略概述</h4>
                基于RSI指标识别超买超卖区域，进行反转交易的量化策略。<br><br>
                
                <h4>⚙️ 策略参数</h4>
                • <strong>RSI周期</strong>：14天<br>
                • <strong>超卖阈值</strong>：30（买入信号）<br>
                • <strong>超买阈值</strong>：70（卖出信号）<br>
                • <strong>止损</strong>：5%<br><br>
                
                <h4>💻 Python代码框架</h4>
                <div style="background: #2c3e50; color: #ecf0f1; padding: 10px; border-radius: 4px; font-family: monospace; font-size: 12px;">
def rsi_strategy(data):<br>
&nbsp;&nbsp;&nbsp;&nbsp;# 计算RSI指标<br>
&nbsp;&nbsp;&nbsp;&nbsp;delta = data['close'].diff()<br>
&nbsp;&nbsp;&nbsp;&nbsp;gain = (delta.where(delta > 0, 0)).rolling(14).mean()<br>
&nbsp;&nbsp;&nbsp;&nbsp;loss = (-delta.where(delta < 0, 0)).rolling(14).mean()<br>
&nbsp;&nbsp;&nbsp;&nbsp;rs = gain / loss<br>
&nbsp;&nbsp;&nbsp;&nbsp;data['RSI'] = 100 - (100 / (1 + rs))<br>
&nbsp;&nbsp;&nbsp;&nbsp;<br>
&nbsp;&nbsp;&nbsp;&nbsp;# 生成交易信号<br>
&nbsp;&nbsp;&nbsp;&nbsp;data['signal'] = 0<br>
&nbsp;&nbsp;&nbsp;&nbsp;data.loc[data['RSI'] < 30, 'signal'] = 1  # 超卖买入<br>
&nbsp;&nbsp;&nbsp;&nbsp;data.loc[data['RSI'] > 70, 'signal'] = -1  # 超买卖出<br>
&nbsp;&nbsp;&nbsp;&nbsp;<br>
&nbsp;&nbsp;&nbsp;&nbsp;return data
                </div>
            </div>
            
            ✅ <strong>策略已生成！</strong>建议先进行历史回测验证效果。
        `;
    } else if (message.includes('macd')) {
        return `
            🔧 <strong>MACD趋势策略创建</strong><br><br>
            
            <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 10px 0;">
                <h4>📋 策略概述</h4>
                利用MACD指标的金叉死叉信号，捕捉中期趋势的量化策略。<br><br>
                
                <h4>⚙️ 策略参数</h4>
                • <strong>快线EMA</strong>：12日指数移动平均<br>
                • <strong>慢线EMA</strong>：26日指数移动平均<br>
                • <strong>信号线</strong>：9日EMA<br>
                • <strong>买入信号</strong>：MACD上穿信号线<br><br>
                
                <h4>💻 Python代码框架</h4>
                <div style="background: #2c3e50; color: #ecf0f1; padding: 10px; border-radius: 4px; font-family: monospace; font-size: 12px;">
def macd_strategy(data):<br>
&nbsp;&nbsp;&nbsp;&nbsp;# 计算MACD指标<br>
&nbsp;&nbsp;&nbsp;&nbsp;ema12 = data['close'].ewm(span=12).mean()<br>
&nbsp;&nbsp;&nbsp;&nbsp;ema26 = data['close'].ewm(span=26).mean()<br>
&nbsp;&nbsp;&nbsp;&nbsp;data['MACD'] = ema12 - ema26<br>
&nbsp;&nbsp;&nbsp;&nbsp;data['Signal'] = data['MACD'].ewm(span=9).mean()<br>
&nbsp;&nbsp;&nbsp;&nbsp;data['Histogram'] = data['MACD'] - data['Signal']<br>
&nbsp;&nbsp;&nbsp;&nbsp;<br>
&nbsp;&nbsp;&nbsp;&nbsp;# 生成交易信号<br>
&nbsp;&nbsp;&nbsp;&nbsp;data['signal'] = 0<br>
&nbsp;&nbsp;&nbsp;&nbsp;data.loc[(data['MACD'] > data['Signal']) & <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(data['MACD'].shift(1) <= data['Signal'].shift(1)), 'signal'] = 1<br>
&nbsp;&nbsp;&nbsp;&nbsp;<br>
&nbsp;&nbsp;&nbsp;&nbsp;return data
                </div>
            </div>
            
            ✅ <strong>策略已生成！</strong>MACD策略适合趋势明显的市场环境。
        `;
    } else {
        return `
            🔧 <strong>量化策略创建助手</strong><br><br>
            
            我可以帮您创建以下类型的量化策略：<br><br>
            
            📈 <strong>技术指标策略</strong>：<br>
            • 双均线交叉策略<br>
            • RSI反转策略<br>
            • MACD趋势策略<br>
            • 布林带均值回归策略<br><br>
            
            📊 <strong>多因子策略</strong>：<br>
            • 价值因子策略<br>
            • 动量因子策略<br>
            • 质量因子策略<br><br>
            
            🤖 <strong>机器学习策略</strong>：<br>
            • 随机森林预测策略<br>
            • LSTM时序预测策略<br><br>
            
            💡 请告诉我您想创建哪种类型的策略，我会为您生成详细的代码和参数配置！
        `;
    }
}

// 策略分析回复生成
function generateStrategyAnalysisResponse(message) {
    if (message.includes('rsi') || message.includes('RSI')) {
        return `
            🔍 <strong>RSI反转策略优缺点分析</strong><br><br>
            
            <div style="background: #e8f5e8; padding: 15px; border-radius: 8px; margin: 10px 0; border-left: 4px solid #28a745;">
                <h4>✅ 策略优点</h4>
                • <strong>操作简单</strong>：RSI指标易于理解和使用<br>
                • <strong>反转及时</strong>：能较好捕捉短期反转机会<br>
                • <strong>风险可控</strong>：有明确的超买超卖界限<br>
                • <strong>适用性强</strong>：适用于大部分震荡市场<br>
                • <strong>资金利用率高</strong>：持仓时间相对较短
            </div>
            
            <div style="background: #ffeaea; padding: 15px; border-radius: 8px; margin: 10px 0; border-left: 4px solid #dc3545;">
                <h4>❌ 策略缺点</h4>
                • <strong>趋势市失效</strong>：强势趋势中容易产生假信号<br>
                • <strong>频繁交易</strong>：可能导致较高的交易成本<br>
                • <strong>参数敏感</strong>：RSI周期和阈值需要优化<br>
                • <strong>滞后性</strong>：基于历史价格，存在一定延迟<br>
                • <strong>单一指标</strong>：缺乏多维度确认信号
            </div>
            
            <div style="background: #fff3cd; padding: 15px; border-radius: 8px; margin: 10px 0; border-left: 4px solid #ffc107;">
                <h4>💡 优化建议</h4>
                • 结合趋势过滤器（如移动平均线）<br>
                • 增加成交量确认信号<br>
                • 设置动态止损机制<br>
                • 考虑市场环境进行参数调整<br>
                • 添加其他技术指标进行确认
            </div>
            
            📊 <strong>适用市场</strong>：震荡市、区间交易<br>
            ⏰ <strong>推荐周期</strong>：日线、小时线<br>
            💰 <strong>预期收益</strong>：中等，胜率较高但单次收益有限
        `;
    } else if (message.includes('双均线') || message.includes('均线')) {
        return `
            🔍 <strong>双均线策略优缺点分析</strong><br><br>
            
            <div style="background: #e8f5e8; padding: 15px; border-radius: 8px; margin: 10px 0; border-left: 4px solid #28a745;">
                <h4>✅ 策略优点</h4>
                • <strong>逻辑清晰</strong>：买卖信号明确，易于执行<br>
                • <strong>趋势跟踪</strong>：能够捕捉中长期趋势机会<br>
                • <strong>经典有效</strong>：经过长期市场验证的成熟策略<br>
                • <strong>参数稳定</strong>：对参数变化不太敏感<br>
                • <strong>适用面广</strong>：适用于多种市场和时间周期
            </div>
            
            <div style="background: #ffeaea; padding: 15px; border-radius: 8px; margin: 10px 0; border-left: 4px solid #dc3545;">
                <h4>❌ 策略缺点</h4>
                • <strong>滞后性强</strong>：信号产生相对较晚<br>
                • <strong>震荡市失效</strong>：横盘震荡时产生大量假信号<br>
                • <strong>回撤较大</strong>：趋势反转时可能面临较大亏损<br>
                • <strong>交易频率低</strong>：错过短期交易机会<br>
                • <strong>止损困难</strong>：缺乏明确的止损点位
            </div>
            
            <div style="background: #fff3cd; padding: 15px; border-radius: 8px; margin: 10px 0; border-left: 4px solid #ffc107;">
                <h4>💡 优化建议</h4>
                • 增加成交量指标确认<br>
                • 结合市场强弱指标过滤<br>
                • 设置固定比例或ATR止损<br>
                • 考虑使用指数移动平均线<br>
                • 添加仓位管理规则
            </div>
            
            📊 <strong>适用市场</strong>：趋势性较强的市场<br>
            ⏰ <strong>推荐周期</strong>：日线、周线<br>
            💰 <strong>预期收益</strong>：中等偏高，胜率中等但盈亏比好
        `;
    } else if (message.includes('macd') || message.includes('MACD')) {
        return `
            🔍 <strong>MACD策略优缺点分析</strong><br><br>
            
            <div style="background: #e8f5e8; padding: 15px; border-radius: 8px; margin: 10px 0; border-left: 4px solid #28a745;">
                <h4>✅ 策略优点</h4>
                • <strong>趋势确认强</strong>：能有效识别趋势转换点<br>
                • <strong>信号质量高</strong>：相对较少的假信号<br>
                • <strong>多重确认</strong>：提供MACD线、信号线、柱状图多重信息<br>
                • <strong>适应性好</strong>：在不同市场环境下表现相对稳定<br>
                • <strong>风险控制</strong>：背离信号提供额外的风险警示
            </div>
            
            <div style="background: #ffeaea; padding: 15px; border-radius: 8px; margin: 10px 0; border-left: 4px solid #dc3545;">
                <h4>❌ 策略缺点</h4>
                • <strong>滞后性明显</strong>：基于移动平均线，反应相对较慢<br>
                • <strong>震荡市效果差</strong>：横盘整理时容易产生误导信号<br>
                • <strong>参数固定</strong>：标准参数未必适合所有品种<br>
                • <strong>缺乏止损</strong>：没有明确的止损机制<br>
                • <strong>信号频率低</strong>：可能错过短期机会
            </div>
            
            <div style="background: #fff3cd; padding: 15px; border-radius: 8px; margin: 10px 0; border-left: 4px solid #ffc107;">
                <h4>💡 优化建议</h4>
                • 结合价格形态分析<br>
                • 添加背离确认机制<br>
                • 设置合理的止损止盈<br>
                • 根据不同品种优化参数<br>
                • 结合市场情绪指标
            </div>
            
            📊 <strong>适用市场</strong>：有明确趋势的市场<br>
            ⏰ <strong>推荐周期</strong>：日线、4小时线<br>
            💰 <strong>预期收益</strong>：中等偏高，信号质量较好
        `;
    } else {
        return `
            🔍 <strong>量化策略分析助手</strong><br><br>
            
            我可以为您分析以下策略的优缺点：<br><br>
            
            📈 <strong>技术指标策略</strong>：<br>
            • RSI反转策略分析<br>
            • 双均线交叉策略分析<br>
            • MACD趋势策略分析<br>
            • 布林带策略分析<br><br>
            
            📊 <strong>量化策略通用分析维度</strong>：<br>
            • ✅ 策略优势与适用场景<br>
            • ❌ 策略缺陷与风险点<br>
            • 💡 优化改进建议<br>
            • 📊 市场适应性评估<br>
            • 💰 收益风险特征<br><br>
            
            💡 请告诉我您想分析哪个具体的量化策略，我会提供详细的优缺点分析！
        `;
    }
}

// ==================== 数据字典功能 ====================

// 表格预览切换功能
function toggleTablePreview(tableId) {
    const preview = document.getElementById(`preview-${tableId}`);
    const button = document.querySelector(`[onclick="toggleTablePreview('${tableId}')"]`);
    const icon = button.querySelector('.btn-icon');
    const btnText = button.querySelector('.btn-text');
    
    if (preview.style.display === 'none' || preview.style.display === '') {
        preview.style.display = 'block';
        icon.textContent = '▲';
        btnText.textContent = '收起详情';
        button.classList.add('active');
    } else {
        preview.style.display = 'none';
        icon.textContent = '▼';
        btnText.textContent = '查看详情';
        button.classList.remove('active');
    }
}

// 数据字典搜索和筛选功能
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('dataSearch');
    const categoryFilter = document.getElementById('categoryFilter');
    
    if (searchInput && categoryFilter) {
        // 搜索功能
        searchInput.addEventListener('input', function() {
            filterDataTables();
        });
        
        // 分类筛选功能
        categoryFilter.addEventListener('change', function() {
            filterDataTables();
        });
    }
});

function filterDataTables() {
    const searchTerm = document.getElementById('dataSearch')?.value.toLowerCase() || '';
    const selectedCategory = document.getElementById('categoryFilter')?.value || 'all';
    
    const categories = document.querySelectorAll('.data-category');
    
    categories.forEach(category => {
        const categoryType = category.getAttribute('data-category');
        const tableCards = category.querySelectorAll('.data-table-card');
        let categoryHasVisibleTables = false;
        
        // 检查分类筛选
        if (selectedCategory !== 'all' && selectedCategory !== categoryType) {
            category.style.display = 'none';
            return;
        }
        
        tableCards.forEach(card => {
            const tableName = card.querySelector('h4').textContent.toLowerCase();
            const tableDescription = card.querySelector('.table-description p')?.textContent.toLowerCase() || '';
            
            // 检查搜索条件
            if (searchTerm === '' || tableName.includes(searchTerm) || tableDescription.includes(searchTerm)) {
                card.style.display = 'block';
                categoryHasVisibleTables = true;
            } else {
                card.style.display = 'none';
            }
        });
        
        // 显示或隐藏分类
        if (categoryHasVisibleTables) {
            category.style.display = 'block';
        } else {
            category.style.display = 'none';
        }
    });
}

// ==================== 数据补充功能 ====================

// 打开数据补充模态框
function openSupplementModal(tableId, tableName) {
    // 创建简单的补数据弹出框
    const startDate = prompt(`为"${tableName || tableId}"补充数据\n\n请输入开始日期 (格式: YYYY-MM-DD):`);
    
    if (!startDate) return; // 用户取消
    
    const endDate = prompt(`请输入结束日期 (格式: YYYY-MM-DD):`);
    
    if (!endDate) return; // 用户取消
    
    // 简单验证日期格式
    const dateRegex = /^\d{4}-\d{2}-\d{2}$/;
    if (!dateRegex.test(startDate) || !dateRegex.test(endDate)) {
        alert('日期格式错误，请使用 YYYY-MM-DD 格式');
        return;
    }
    
    // 验证日期有效性
    if (new Date(startDate) > new Date(endDate)) {
        alert('开始日期不能晚于结束日期');
        return;
    }
    
    // 模拟补数据过程
    const confirmed = confirm(`确认为"${tableName || tableId}"补充数据？\n\n时间范围：${startDate} 至 ${endDate}\n\n点击确定开始补数据...`);
    
    if (confirmed) {
        showNotification(`正在为"${tableName || tableId}"补充数据 (${startDate} ~ ${endDate})...`);
        
        // 模拟补数据完成
        setTimeout(() => {
            showNotification(`"${tableName || tableId}"数据补充完成！`);
        }, 2000);
    }
}

// 简化的补数据功能完成，其他复杂功能已移除