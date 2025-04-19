<script setup lang="ts">
import { defineProps, ref, reactive, markRaw, onMounted, computed, onUnmounted } from "vue";
import { 
  School, 
  User, 
  Medal, 
  WindPower, 
  DataAnalysis, 
  Connection, 
  Lightning
} from "@element-plus/icons-vue";
// 如果需要router，请确保安装了vue-router
// import { useRouter } from 'vue-router'

const props = defineProps({
  isDark: {
    type: Boolean,
    required: true
  },
  windowsHeight: {
    type: Number,
    required: true
  },
  windowsWidth: {
    type: Number,
    required: true
  }
});

// const router = useRouter()
const teamMembers = [
  {
    name: '李奕帆',
    role: '项目负责人',
    department: '信息工程学院',
    major: '计算机科学与技术（卓越工程师）',
    avatar: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png'
  },
  {
    name: '刘濮瑜',
    role: '团队成员',
    department: '未来交通学院',
    major: '工科试验班（交通工程）',
    avatar: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png'
  },
  {
    name: '解政恺',
    role: '团队成员',
    department: '信息工程学院',
    major: '计算机科学与技术',
    avatar: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png'
  },
  {
    name: '谢珂',
    role: '团队成员',
    department: '信息工程学院',
    major: '计算机科学与技术',
    avatar: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png'
  },
  {
    name: '黄瑞燊',
    role: '团队成员',
    department: '信息工程学院',
    major: '计算机科学与技术（卓越工程师）',
    avatar: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png'
  }
];

const features = [
  {
    icon: WindPower,
    title: '风机管理',
    description: '支持多风机信息管理，直观展示风机运行状态'
  },
  {
    icon: DataAnalysis,
    title: '数据可视化',
    description: '强大的数据分析工具，帮助您理解风电数据'
  },
  {
    icon: Connection,
    title: '智能预测',
    description: '基于先进深度学习模型的风电功率预测系统'
  },
  {
    icon: Lightning,
    title: '高效训练',
    description: '优化的模型训练流程，提供精准的预测结果'
  }
];

// 元素引用
const particlesContainer = ref<HTMLElement | null>(null);

// 创建精简的粒子效果
const createParticles = () => {
  const container = particlesContainer.value;
  if (!container) return;
  
  const particleCount = 12; // 减少粒子数量
  
  for (let i = 0; i < particleCount; i++) {
    const particle = document.createElement('div');
    particle.className = 'particle';
    
    // 随机位置和大小
    const size = Math.random() * 6 + 2; // 更小的粒子
    const posX = Math.random() * 100;
    const posY = Math.random() * 100;
    const delay = Math.random() * 3;
    const duration = Math.random() * 8 + 10;
    
    particle.style.width = `${size}px`;
    particle.style.height = `${size}px`;
    particle.style.left = `${posX}%`;
    particle.style.top = `${posY}%`;
    particle.style.animationDelay = `${delay}s`;
    particle.style.animationDuration = `${duration}s`;
    
    container.appendChild(particle);
  }
};

// 添加简单的鼠标交互
const addMouseInteraction = () => {
  const container = particlesContainer.value;
  if (!container) return;
  
  container.addEventListener('mousemove', (e: MouseEvent) => {
    const mouseX = e.clientX / window.innerWidth;
    const mouseY = e.clientY / window.innerHeight;
    
    const particles = container.querySelectorAll('.particle');
    particles.forEach((particle) => {
      if (particle instanceof HTMLElement) {
        const offsetX = (mouseX - 0.5) * 10;
        const offsetY = (mouseY - 0.5) * 10;
        particle.style.transform = `translate(${offsetX}px, ${offsetY}px)`;
      }
    });
  });
};

// 清理粒子
const cleanupParticles = () => {
  const container = particlesContainer.value;
  if (!container) return;
  
  const particles = container.querySelectorAll('.particle');
  particles.forEach(particle => {
    particle.remove();
  });
};

// 初始化
onMounted(() => {
  createParticles();
  addMouseInteraction();
  
  // 添加滚动动画
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('animate');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1 });
  
  // 观察团队成员
  const teamMemberElements = document.querySelectorAll('.team-member');
  teamMemberElements.forEach(item => {
    observer.observe(item);
  });
});

onUnmounted(() => {
  cleanupParticles();
});
</script>

<template>
  <div class="about-container" :class="{ 'dark-mode': isDark }">
    <!-- 英雄部分 -->
    <section class="hero-section">
      <div class="particles-container" ref="particlesContainer"></div>
      <div class="logo-container">
        <div class="logo-background"></div>
        <img src="../assets/static/img/deepwind-icon.png" alt="DeepWind Logo" />
      </div>
      <h1 class="hero-title">风起云算·智风 DeepWind</h1>

      <p class="hero-subtitle">
        融合Hadoop大数据生态、AI赋能、K8s云原生的三位一体风电预测系统
      </p>
      <div class="decorative-line"></div>
    </section>

    <!-- 项目介绍 -->
    <section class="about-section">
      <div class="section-header">
        <h2 class="section-title">关于我们的项目</h2>
        <div class="title-underline"></div>
      </div>
      <div class="section-content">
        <p class="about-text">
          本项目为中国大学生计算机设计大赛——软件应用与开发赛道参赛作品，
        </p>
        <p class="about-text">
          我们来自长安大学信息工程学院和未来交通学院。
        </p>   


        
        <div class="features-grid">
          <div v-for="(feature, index) in features" :key="index" class="feature-card">
            <div class="feature-card-inner">
              <div class="feature-icon">
                <el-icon><component :is="feature.icon" /></el-icon>
                <div class="icon-glow"></div>
              </div>
              <h3 class="feature-title">{{ feature.title }}</h3>
              <p class="feature-description">{{ feature.description }}</p>
              <div class="feature-shine"></div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 团队介绍 -->
    <section class="team-section">
      <div class="section-header">
        <h2 class="section-title">团队成员</h2>
        <div class="title-underline"></div>
      </div>
      <div class="section-content">
        <div class="team-grid">
          <div v-for="(member, index) in teamMembers" :key="index" class="team-member animate" :style="{animationDelay: `${index * 0.1}s`}">
            <div class="member-card">
              <div class="member-avatar">
                <div class="avatar-border"></div>
                <img :src="member.avatar" alt="头像" />
                <div class="member-badge" v-if="member.role === '项目负责人'">
                  <el-icon><Medal /></el-icon>
                </div>
              </div>
              <div class="member-info">
                <h3 class="member-name">{{ member.name }}</h3>
                <div class="member-role">{{ member.role }}</div>
                <div class="member-details">
                  <div class="detail-item">
                    <el-icon><School /></el-icon>
                    <span>{{ member.department }}</span>
                  </div>
                  <div class="detail-item">
                    <el-icon><User /></el-icon>
                    <span>{{ member.major }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 页脚 - 简化版 -->
    <footer class="footer">
      <div class="footer-container">
        <div class="footer-logo">
          <img src="../assets/static/img/deepwind-icon.png" alt="DeepWind Logo">
          <div class="footer-logo-text">DeepWind</div>
        </div>
        <p class="footer-description">
          基于深度学习、大数据生态与云原生技术，为风电场提供精准的风能预测。
        </p>
        <p class="copyright">© 2025 长安大学 信息工程学院 未来交通学院</p>
      </div>
    </footer>
  </div>
</template>

<style scoped>
/* 主要容器样式 */
.about-page {
  font-family: 'Helvetica Neue', Arial, sans-serif;
  color: #333;
  overflow-x: hidden;
}

/* 英雄区域样式 */
.hero-section {
  position: relative;
  height: 600px;
  overflow: hidden;
  background: linear-gradient(135deg, #e6f7ff 0%, #b3e0ff 50%, #80c1ff 100%);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  padding: 2rem;
}

/* 网格纹理背景 */
.hero-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image:
      linear-gradient(rgba(255,255,255,0.1) 1px, transparent 1px),
      linear-gradient(90deg, rgba(255,255,255,0.1) 1px, transparent 1px);
  background-size: 50px 50px;
  z-index: 1;
}

/* 粒子容器 */
.particles-container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
  z-index: 0;
  opacity: 0.5;
}

/* 粒子样式 */
.particle {
  position: absolute;
  background: radial-gradient(circle at center, rgba(200, 230, 255, 0.8) 0%, rgba(150, 200, 255, 0) 70%);
  border-radius: 50%;
  opacity: 0.6;
  pointer-events: none;
  animation: float 15s infinite ease-in-out;
  box-shadow: 0 0 5px rgba(150, 200, 255, 0.3);
}

@keyframes float {
  0%, 100% {
    transform: translateY(0) translateX(0);
    opacity: 0.2;
  }
  25% {
    transform: translateY(-15px) translateX(10px);
    opacity: 0.6;
  }
  50% {
    transform: translateY(-25px) translateX(-10px);
    opacity: 0.3;
  }
  75% {
    transform: translateY(-10px) translateX(15px);
    opacity: 0.5;
  }
}

/* 标志样式 */
.logo-container {
  position: relative;
  z-index: 3;
  margin-bottom: 2rem;
}

.logo {
  width: 120px;
  height: 120px;
  object-fit: contain;
  animation: pulse 3s infinite alternate;
  filter: drop-shadow(0 0 15px rgba(100, 180, 255, 0.8));
}

@keyframes pulse {
  0% {
    transform: scale(1);
    filter: drop-shadow(0 0 10px rgba(100, 180, 255, 0.6));
  }
  100% {
    transform: scale(1.05);
    filter: drop-shadow(0 0 25px rgba(100, 180, 255, 0.9));
  }
}

/* 标题样式 */
.hero-title {
  font-size: 3.5rem;
  font-weight: 800;
  margin-bottom: 1rem;
  background: linear-gradient(to right, #0066cc, #4da6ff);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  text-shadow: 0 0 15px rgba(0, 102, 204, 0.2);
  position: relative;
  z-index: 3;
}

/* 副标题样式 */
.hero-subtitle {
  font-size: 1.5rem;
  max-width: 700px;
  margin: 0 auto 2rem;
  color: #0066cc;
  position: relative;
  z-index: 3;
  line-height: 1.6;
}

/* 项目介绍部分 */
.about-section {
  padding: 80px 0;
  background: #f5f9ff;
}

.section-header {
  text-align: center;
  margin-bottom: 50px;
}

.section-title {
  font-size: 2.2rem;
  color: #0066cc;
  margin-bottom: 15px;
  position: relative;
  display: inline-block;
}

.title-underline {
  width: 60px;
  height: 3px;
  background: linear-gradient(90deg, #4da6ff, #0066cc);
  margin: 0 auto;
  border-radius: 3px;
}

.about-text {
  max-width: 800px;
  margin: 0 auto 50px;
  font-size: 1.1rem;
  line-height: 1.8;
  color: #333;
  text-align: center;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 30px;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.feature-card {
  background: white;
  border-radius: 15px;
  padding: 30px;
  box-shadow: 0 10px 30px rgba(0, 102, 204, 0.1);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.feature-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 15px 40px rgba(0, 102, 204, 0.15);
}

.feature-icon {
  width: 70px;
  height: 70px;
  background: linear-gradient(135deg, #e6f7ff, #b3e0ff);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 20px;
  position: relative;
}

.feature-icon .el-icon {
  font-size: 32px;
  color: #0066cc;
}

.icon-glow {
  position: absolute;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background: radial-gradient(circle at center, rgba(0, 102, 204, 0.2) 0%, transparent 70%);
  animation: pulse 2s infinite;
}

.feature-title {
  font-size: 1.3rem;
  color: #0066cc;
  margin-bottom: 15px;
  text-align: center;
}

.feature-description {
  color: #666;
  line-height: 1.6;
  text-align: center;
  font-size: 0.95rem;
}

.feature-shine {
  position: absolute;
  top: 0;
  left: -100%;
  width: 50%;
  height: 100%;
  background: linear-gradient(
      90deg,
      transparent,
      rgba(255, 255, 255, 0.2),
      transparent
  );
  transform: skewX(-25deg);
  transition: 0.5s;
}

.feature-card:hover .feature-shine {
  left: 150%;
}

/* 联系部分样式 */
.contact-section {
  display: none;
}

/* 团队成员部分 */
.team-section {
  padding: 80px 0;
  background: linear-gradient(135deg, #f0f7ff 0%, #ffffff 100%);
  position: relative;
  overflow: hidden;
}

.team-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 200px;
  background: linear-gradient(to bottom, rgba(179, 224, 255, 0.2), transparent);
  z-index: 1;
}

.team-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 40px;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  position: relative;
  z-index: 2;
}

.team-member {
  transition: all 0.4s ease;
  transform: translateY(30px);
  opacity: 0;
}

.team-member.animate {
  opacity: 1;
  transform: translateY(0);
}

.team-member:hover {
  transform: translateY(-10px);
}

.member-card {
  background: white;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 15px 35px rgba(0, 102, 204, 0.12);
  position: relative;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  height: 100%;
  border: 1px solid rgba(77, 166, 255, 0.1);
  padding-top: 30px;
}

.member-card:hover {
  box-shadow: 0 20px 40px rgba(0, 102, 204, 0.2);
  border-color: rgba(77, 166, 255, 0.3);
}

.member-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 120px;
  background: linear-gradient(135deg, #e6f7ff, #b3e0ff);
  z-index: 0;
  opacity: 0.7;
}

.member-avatar {
  position: relative;
  padding-top: 60%;
  overflow: hidden;
  background: linear-gradient(135deg, #e6f7ff, #b3e0ff);
  margin: 0 auto;
  width: 60%;
  border-radius: 50%;
  margin-top: 20px;
  box-shadow: 0 10px 25px rgba(0, 102, 204, 0.15);
  z-index: 1;
}

.avatar-border {
  position: absolute;
  top: 4px;
  left: 4px;
  right: 4px;
  bottom: 4px;
  border: 2px solid rgba(255, 255, 255, 0.8);
  border-radius: 50%;
  z-index: 1;
  box-shadow: inset 0 0 15px rgba(77, 166, 255, 0.3);
}

.avatar-border::after {
  content: '';
  position: absolute;
  top: -2px;
  left: -2px;
  right: -2px;
  bottom: -2px;
  border-radius: 50%;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.2), transparent);
  z-index: 0;
}

.member-avatar img {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: all 0.5s ease;
  border-radius: 50%;
  filter: contrast(1.05) brightness(1.02);
}

.member-card:hover .member-avatar img {
  transform: scale(1.08);
}

.member-badge {
  position: absolute;
  bottom: 5px;
  right: 15%;
  width: 36px;
  height: 36px;
  background: linear-gradient(135deg, #0066cc, #4da6ff);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  z-index: 2;
  box-shadow: 0 4px 10px rgba(0, 102, 204, 0.3);
  border: 2px solid white;
}

.member-badge .el-icon {
  font-size: 20px;
}

.member-info {
  padding: 25px 20px 30px;
  text-align: center;
  background: white;
  flex: 1;
  display: flex;
  flex-direction: column;
  position: relative;
  z-index: 1;
  margin-top: 10px;
}

.member-name {
  margin: 0 0 5px;
  font-size: 1.4rem;
  color: #0066cc;
  font-weight: 700;
  text-shadow: 0 1px 2px rgba(0, 102, 204, 0.1);
}

.member-role {
  color: #4da6ff;
  font-size: 1rem;
  margin-bottom: 20px;
  font-weight: 500;
  position: relative;
  display: inline-block;
  padding-bottom: 10px;
}

.member-role::after {
  content: '';
  position: absolute;
  left: 50%;
  bottom: 0;
  width: 40px;
  height: 2px;
  background: linear-gradient(90deg, transparent, #4da6ff, transparent);
  transform: translateX(-50%);
}

.member-details {
  display: flex;
  flex-direction: column;
  gap: 15px;
  margin-top: auto;
}

.detail-item {
  display: flex;
  align-items: center;
  color: #666;
  font-size: 1rem;
  line-height: 1.6;
  padding: 8px 15px;
  background: rgba(230, 247, 255, 0.3);
  border-radius: 8px;
  transition: all 0.3s ease;
}

.detail-item span {
  font-weight: 600;
  color: #333;
}

.detail-item:hover {
  background: rgba(230, 247, 255, 0.5);
  transform: translateX(5px);
}

.detail-item .el-icon {
  color: #4da6ff;
  margin-right: 12px;
  font-size: 20px;
  flex-shrink: 0;
}

/* 页脚样式 */
.footer {
  background: linear-gradient(to bottom, #e6f7ff, #b3e0ff);
  color: #333;
  padding: 40px 0;
  position: relative;
  overflow: hidden;
  text-align: center;
}

.footer-container {
  max-width: 900px;
  margin: 0 auto;
  padding: 0 20px;
}

.footer-logo {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 25px;
}

.footer-logo img {
  width: 42px;
  height: 42px;
  margin-right: 15px;
  filter: drop-shadow(0 0 8px rgba(3, 169, 244, 0.3));
  transition: all 0.3s ease;
}

.footer-logo:hover img {
  transform: rotate(15deg);
  filter: drop-shadow(0 0 12px rgba(3, 169, 244, 0.5));
}

.footer-logo-text {
  font-size: 1.5rem;
  font-weight: 700;
  color: #0066cc;
  background: linear-gradient(90deg, #0066cc, #4da6ff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.footer-description {
  color: #0066cc;
  opacity: 0.8;
  line-height: 1.6;
  margin-bottom: 20px;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

.copyright {
  color: #0066cc;
  opacity: 0.7;
  font-size: 0.9rem;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.team-member.animate {
  animation: fadeInUp 0.6s ease forwards;
}

@media (max-width: 768px) {
  .team-grid {
    gap: 30px;
  }

  .member-avatar {
    width: 55%;
    padding-top: 55%;
  }

  .detail-item {
    font-size: 0.95rem;
    padding: 6px 12px;
  }
}

@media (max-width: 576px) {
  .hero-title {
    font-size: 2.5rem;
  }

  .hero-subtitle {
    font-size: 1.2rem;
  }

  .section-title {
    font-size: 1.8rem;
  }

  .team-grid {
    gap: 25px;
  }

  .member-avatar {
    width: 50%;
    padding-top: 50%;
  }

  .member-card::before {
    height: 100px;
  }

  .detail-item {
    font-size: 0.9rem;
    padding: 5px 10px;
  }
}

/* 动画延迟 */
.team-member:nth-child(1) { animation-delay: 0.1s; }
.team-member:nth-child(2) { animation-delay: 0.2s; }
.team-member:nth-child(3) { animation-delay: 0.3s; }
.team-member:nth-child(4) { animation-delay: 0.4s; }
.team-member:nth-child(5) { animation-delay: 0.5s; }
</style>