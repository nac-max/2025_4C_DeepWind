<script setup lang="ts">
import {ChatLineSquare, Warning, ArrowRight, Connection, DataBoard, Finished, Histogram, Opportunity} from "@element-plus/icons-vue";
</script>

<template>
  <div class="guide-container">
    <!-- 标题区域 -->
    <header class="guide-header">
      <div class="title-container">
        <h1 class="guide-title">快速入门 DeepWind</h1>
        <p class="guide-subtitle">
          我应该如何使用此系统？
          <span class="highlight-text">让我们一起探索吧！</span>
        </p>
      </div>
      <div class="header-decoration"></div>
    </header>
    
    <!-- 简介部分 -->
    <section class="guide-intro">
      <p class="intro-text">风机功率预测共分为以下五步:</p>
      
      <div class="steps-container">
        <el-steps :active="1" align-center class="custom-steps">
          <el-step title="第一步" description="添加风机信息" :icon="Opportunity" />
          <el-step title="第二步" description="上传风机数据" :icon="DataBoard" />
          <el-step title="第三步" description="训练预测模型" :icon="Connection" />
          <el-step title="第四步" description="下达预测任务" :icon="Histogram" />
          <el-step title="第五步" description="开始预测！" :icon="Finished" />
        </el-steps>
      </div>
      
      <p class="intro-text">我们致力于帮助您在最短时间内掌握本系统，完成您的风电预测任务。</p>
      
      <div class="tip-card">
        <el-icon class="tip-icon"><ChatLineSquare /></el-icon>
        <p class="tip-text">您可以随时点击右上角的导航栏，前往预测系统实践！</p>
      </div>
    </section>
    
    <!-- 第一步 -->
    <section class="guide-section">
      <div class="section-header">
        <div class="step-number">01</div>
        <h2 class="section-title">添加风机信息</h2>
      </div>
      
      <p class="section-text">风机管理页面列出了系统中所有的上线风机信息.</p>
      
      <div class="image-container">
        <img
          class="guide-image"
          src="../../assets/static/img/guide/quick_start/1-1.png"
          alt="风机管理页面"
        />
      </div>
      
      <p class="section-text">
        通过单击右上角的
        <el-tag type="success" class="custom-tag">上传风机信息</el-tag>
        按钮，您可以添加风机信息至系统中。
      </p>
      
      <div class="image-container centered">
        <img
          class="guide-image medium"
          src="../../assets/static/img/guide/quick_start/1-2.png"
          alt="风机信息表单"
        />
      </div>
      
      <p class="section-text">
        您可以在
        <el-tag type="info" class="custom-tag">风机信息表单</el-tag>
        中上传风机模型和训练数据，
        也可以在信息表单中就提前完成第二步与第三步的一部分-添加风机模型及上传训练数据。
      </p>
      
      <p class="section-text">
        如果您有任何疑问，可通过<span class="highlight-text">li.yifan2004@hotmail.com</span> 联系我们
      </p>
      
      <p class="section-text">
        在上传风机信息表单后，您应该会看到风机管理页面中成功添加一条风机信息记录，它是您所添加的风机。
      </p>
      
      <p class="section-text">
        至此，您已经完成了第一步-添加风机信息。
      </p>
    </section>
    
    <!-- 第二步 -->
    <section class="guide-section">
      <div class="section-header">
        <div class="step-number">02</div>
        <h2 class="section-title">上传风机数据</h2>
      </div>
      
      <p class="section-text">
        在预测系统的各个部分都可以进行上传风机数据的操作，只要看到有
        <el-tag type="info" class="custom-tag">上传数据</el-tag>按钮，就可以通过单击按钮，呼出上传数据表单，进行数据上传操作。
        但是我们推荐您在数据空间页面进行上传操作。
      </p>
      
      <div class="image-container">
        <img
          class="guide-image"
          src="../../assets/static/img/guide/quick_start/2-1.png"
          alt="数据空间页面"
        />
      </div>
      
      <p class="section-text">
        我们先来看看上传至预测系统的数据类型及格式。
      </p>
      
      <div class="data-types">
        <p class="section-text">
          风电预测系统中存储的数据类型一共有三种，分别是
          <el-tag effect="plain" type="success" class="custom-tag">训练数据</el-tag>、
          <el-tag effect="plain" class="custom-tag">预测数据</el-tag>
          和
          <el-tag effect="plain" type="info" class="custom-tag">预测结果</el-tag>；
          它们是一系列的.csv文件或.xlxs文件，每个文件中包含了一定时间范围内的风机数据。
        </p>
        
        <p class="section-text">
          <el-tag effect="plain" type="success" class="custom-tag">训练数据</el-tag>
          被用来训练风机的预测模型，预测模型的准确度一大部分取决于训练数据的质量。
          而
          <el-tag effect="plain" class="custom-tag">预测数据</el-tag>
          则用来进行风电未来功率的预测任务，预测数据的质量也会一定程度上影响预测结果的准确度。
        </p>
        
        <p class="section-text">
          对于这两类数据来说，它们都将由您上传至预测系统，来为系统提供"燃料"。
          而最后的
          <el-tag effect="plain" type="info" class="custom-tag">预测结果</el-tag>
          则是由系统生成的预测结果，您可以在预测中心页面中查看预测结果，并下载相应数据。
        </p>
      </div>
      
      <p class="section-text">
        需要注意的是，这些数据的上传格式是有要求的，请您上传符合格式要求的数据。
        对于训练数据和预测数据，您可以在数据空间页面中下载模板文件，来查看数据格式要求。
      </p>
      
      <div class="image-container">
        <img
          class="guide-image"
          src="../../assets/static/img/guide/quick_start/2-2.png"
          alt="数据空间页面"
        />
      </div>
      
      <p class="section-text conclusion-text">
        至此您已经知晓了第二步-上传风机数据的方方面面，接下来是精彩的部分了---训练风机模型。
      </p>
    </section>
    
    <!-- 第三步 -->
    <section class="guide-section">
      <div class="section-header">
        <div class="step-number">03</div>
        <h2 class="section-title">训练风机模型</h2>
      </div>
      
      <p class="section-text">
        在风机模型页面，您可以查看到所有风机拥有的预测模型信息，并且您还可以在此页面
        进行风机模型的添加及训练功能；不过，在此之前，您需要先了解一下风机模型的类型。
      </p>
      
      <div class="model-types-container">
        <h3 class="model-section-title">预测模型类型</h3>
        
        <div class="model-cards">
          <div class="model-card">
            <div class="model-card-header">
              <el-tag effect="plain" class="model-tag">MLP</el-tag>
              <div class="model-rating">
                <span class="model-rating-label">速度</span>
                <div class="rating-bars">
                  <span class="rating-bar filled"></span>
                  <span class="rating-bar filled"></span>
                  <span class="rating-bar filled"></span>
                </div>
              </div>
            </div>
            <div class="model-card-body">
              <p class="model-description">仅需要未来天气预报数据即可进行预测，计算速度快，适合实时预测场景。</p>
            </div>
          </div>
          
          <div class="model-card">
            <div class="model-card-header">
              <el-tag effect="plain" class="model-tag">GCN+LSTM</el-tag>
              <div class="model-rating">
                <span class="model-rating-label">平衡</span>
                <div class="rating-bars">
                  <span class="rating-bar filled"></span>
                  <span class="rating-bar filled"></span>
                  <span class="rating-bar"></span>
                </div>
              </div>
            </div>
            <div class="model-card-body">
              <p class="model-description">仅需要风机历史数据即可进行预测，适合具有明显时序特征的场景。</p>
            </div>
          </div>
          
          <div class="model-card">
            <div class="model-card-header">
              <el-tag effect="plain" class="model-tag">GCN+LSTM+MLP</el-tag>
              <div class="model-rating">
                <span class="model-rating-label">精度</span>
                <div class="rating-bars">
                  <span class="rating-bar filled"></span>
                  <span class="rating-bar filled"></span>
                  <span class="rating-bar filled"></span>
                </div>
              </div>
            </div>
            <div class="model-card-body">
              <p class="model-description">结合风机历史数据和未来天气预报数据进行预测，精度最高，适合对预测准确度要求较高的场景。</p>
            </div>
          </div>
        </div>
      </div>

      <p class="section-text">
        您可以根据实际应用场景和需求选择合适的预测模型。通常情况下，如果对预测精度要求较高，推荐使用GCN+LSTM+MLP模型；如果对预测速度有较高要求，则可以选择MLP模型。
      </p>
      
      <div class="image-container">
        <img
          class="guide-image"
          src="../../assets/static/img/guide/quick_start/3-1.png"
          alt="风机模型页面"
        />
      </div>
      
      <p class="section-text">
        您可以通过单击风机卡片右上角的<el-tag type="success" class="custom-tag">添加预测模型</el-tag>按钮，
        来为一个风机添加新预测模型；在简单填写模型信息表单并上传后，你的新模型就会被添加到风机模型列表中，
        并且蓄势待发，准备开始训练。
      </p>
      
      <div class="image-container centered">
        <img
          class="guide-image medium"
          src="../../assets/static/img/guide/quick_start/3-2.png"
          alt="添加预测模型"
        />
      </div>
      
      <p class="section-text">
        而对于通过其他方式添加的风机模型，在开始训练之前，你可能需要先为它选择训练数据；
        你还可以同时选择多个训练数据，模型会依次以所选数据进行训练。
      </p>
      
      <p class="section-text">
        在确保万事俱备后，点击模型的
        <el-tag class="custom-tag">开始训练</el-tag>按钮，即可开始训练。
      </p>
      
      <div class="warning-card">
        <el-icon class="warning-icon"><Warning /></el-icon>
        <p class="warning-text">请注意，训练预测模型是一个十分耗时的过程，需要占用系统大量计算量，因此请不要同时训练多个模型。</p>
      </div>
      
      <div class="process-info">
        <div class="process-icon">
          <el-icon><Connection /></el-icon>
        </div>
        <div class="process-details">
          <h4 class="process-title">训练进度跟踪</h4>
          <p class="process-description">
            在开始训练后，模型的右方会出现当前训练的进度条，显示训练进度。
            训练完成时，系统右上方将会弹出消息框进行提示。
          </p>
        </div>
      </div>
      
      <p class="section-text">
        在开始训练后，模型的右方会出现当前训练的进度条，来显示当前的训练进度,
        训练完成时，系统右上方将会弹出消息框来进行提示。
      </p>
      
      <p class="section-text conclusion-text">
        恭喜！至此您以完成了第三步-训练风机模型的所有操作，接下来是下达预测任务部分。
      </p>
    </section>
    
    <!-- 第四步 -->
    <section class="guide-section">
      <div class="section-header">
        <div class="step-number">04</div>
        <h2 class="section-title">下达预测任务</h2>
      </div>
      
      <p class="section-text">
        模型训练完成后，便可进行预测任务的下达，您可以通过单击模型右侧的
        <el-tag class="custom-tag">预测</el-tag>
        按钮，呼出预测任务下达表单，在填写完表单信息并上传后，即可下达预测任务。
      </p>
      
      <div class="task-workflow">
        <div class="workflow-step">
          <div class="workflow-icon">1</div>
          <div class="workflow-content">
            <h4 class="workflow-title">单击模型的"预测"按钮</h4>
            <p class="workflow-description">呼出预测任务下达表单</p>
          </div>
        </div>
        <div class="workflow-arrow">
          <el-icon><ArrowRight /></el-icon>
        </div>
        <div class="workflow-step">
          <div class="workflow-icon">2</div>
          <div class="workflow-content">
            <h4 class="workflow-title">填写表单信息</h4>
            <p class="workflow-description">设置预测参数与配置</p>
          </div>
        </div>
        <div class="workflow-arrow">
          <el-icon><ArrowRight /></el-icon>
        </div>
        <div class="workflow-step">
          <div class="workflow-icon">3</div>
          <div class="workflow-content">
            <h4 class="workflow-title">提交表单</h4>
            <p class="workflow-description">系统将自动开始预测任务</p>
          </div>
        </div>
      </div>
      
      <div class="image-container centered">
        <img
          class="guide-image medium"
          src="../../assets/static/img/guide/quick_start/4-1.png"
          alt="下达预测任务"
        />
      </div>
      
      <p class="section-text">
        您也可以在风机管理页面进行预测任务的下达，只需单击风机卡片右上角的开始预测即可，
        但我们推荐您在预测中心页面，完成相应的操作。
      </p>
      
      <div class="image-container">
        <img
          class="guide-image"
          src="../../assets/static/img/guide/quick_start/4-2.png"
          alt="风机管理页面"
        />
      </div>
      
      <p class="section-text">
        您可以在预测中心页面查看当前所有的预测任务，或删除已有任务，
        预测任务的左端环形进度条显示了当前任务的进行程度。
      </p>
      
      <p class="section-text">
        通过单击预测任务卡片右上角的
        <el-tag class="custom-tag">开始预测</el-tag>按钮，即可进行预测。
      </p>
      
      <p class="section-text">
        对于已完成的预测任务，您可以通过单击预测任务卡片右上角的
        <el-tag class="custom-tag">数据可视化</el-tag>
        按钮，来查看预测结果。或点击右小角的
        <el-tag type="success" class="custom-tag">按钮</el-tag>
        ，来下载预测结果文件。
      </p>
      
      <div class="image-container">
        <img
          class="guide-image"
          src="../../assets/static/img/guide/quick_start/4-3.png"
          alt="数据可视化页面"
        />
      </div>
      
      <p class="section-text">
        对了，您还可以在数据空间页面对训练数据及预测数据进行数据可视化，以便更好地了解数据情况。
        数据可视化页面十分有趣，您可以随心探索下它的功能妙用。
      </p>
      
      <div class="visualization-features">
        <h3 class="feature-section-title">数据可视化功能</h3>
        <div class="feature-cards">
          <div class="feature-card">
            <div class="feature-icon">
              <el-icon><DataBoard /></el-icon>
            </div>
            <h4 class="feature-title">实时数据展示</h4>
            <p class="feature-description">查看风机实时运行数据，及时了解风机状态</p>
          </div>
          
          <div class="feature-card">
            <div class="feature-icon">
              <el-icon><Histogram /></el-icon>
            </div>
            <h4 class="feature-title">历史趋势分析</h4>
            <p class="feature-description">分析历史数据趋势，发现潜在规律</p>
          </div>
          
          <div class="feature-card">
            <div class="feature-icon">
              <el-icon><Finished /></el-icon>
            </div>
            <h4 class="feature-title">预测结果对比</h4>
            <p class="feature-description">对比预测结果与实际值，评估预测精度</p>
          </div>
        </div>
      </div>
      
      <p class="section-text conclusion-text">
        恭喜你！你已经完成了第四步，预测任务下达部分，接下来是最后一步，马上就要结束了！
      </p>
    </section>
    
    <!-- 第五步 -->
    <section class="guide-section final-section">
      <div class="section-header">
        <div class="step-number">05</div>
        <h2 class="section-title">开始预测</h2>
      </div>
      
      <div class="final-content">
        <div class="surprise-container">
          <el-icon class="surprise-icon"><Opportunity /></el-icon>
          <p class="section-text surprise-text">
            等等...我们搞错了，这里没有
            <el-tag effect="plain" type="info" class="custom-tag">第五步</el-tag>
          </p>
        </div>
        
        <p class="section-text">
          您已经完成了指南的所有内容。
          现在，您已经掌握了使用DeepWind进行风机功率预测的全部流程。
        </p>
        
        <h3 class="next-title">接下来是什么？</h3>
        
        <div class="next-steps">
          <div class="next-step">
            <div class="next-step-number">01</div>
            <p class="next-step-text">尝试系统的其他功能，发掘更多可能性</p>
          </div>
          
          <div class="next-step">
            <div class="next-step-number">02</div>
            <p class="next-step-text">与我们的AI助手小风交流，获取更多帮助</p>
          </div>
          
          <div class="next-step">
            <div class="next-step-number">03</div>
            <p class="next-step-text">探索数据可视化功能，深入理解您的数据</p>
          </div>
        </div>
        
        <p class="section-text">
          我们已经为您提供了最基础的指导，接下来的区域需要您去
          <span class="highlight-text">自行探索</span>
        </p>
        
        <div class="farewell-container">
          <p class="farewell-text">
            感谢您使用DeepWind系统
          </p>
          <p class="support-text">
            如有任何问题，请随时联系我们的支持团队
          </p>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
/* 基础变量 */
:root {
  --primary-color: #4557e5;
  --primary-light: rgba(69, 87, 229, 0.1);
  --primary-hover: #3a4cd9;
  --secondary-color: #2d96e8;
  --secondary-light: rgba(45, 150, 232, 0.1);
  --success-color: #67c23a;
  --warning-color: #e6a23c;
  --info-color: #909399;
  --text-primary: #1a202c;
  --text-secondary: #4a5568;
  --text-tertiary: #718096;
  --bg-light: #f8faff;
  --bg-dark: #1a1e2e;
  --card-bg: #ffffff;
  --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 16px rgba(0, 0, 0, 0.08);
  --border-radius-sm: 6px;
  --border-radius-md: 12px;
  --border-radius-lg: 20px;
  --transition-normal: all 0.3s ease;
}

/* 容器样式 */
.guide-container {
  max-width: 900px;
  margin: 0 auto;
  padding: 20px;
  color: var(--text-primary);
  font-family: 'PingFang SC', 'Helvetica Neue', Arial, sans-serif;
}

/* 标题区域 */
.guide-header {
  position: relative;
  margin-bottom: 40px;
  padding-bottom: 20px;
}

.title-container {
  position: relative;
  z-index: 1;
}

.guide-title {
  font-size: 36px;
  font-weight: 700;
  margin: 0 0 16px 0;
  background: linear-gradient(135deg, #4557e5, #2d96e8);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  letter-spacing: 0.5px;
}

.guide-subtitle {
  font-size: 18px;
  color: var(--text-secondary);
  margin: 0;
  line-height: 1.6;
}

.header-decoration {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 1px;
  background: linear-gradient(90deg, 
    rgba(69, 87, 229, 0.1), 
    rgba(45, 150, 232, 0.8), 
    rgba(69, 87, 229, 0.1)
  );
}

/* 高亮文本 */
.highlight-text {
  background: linear-gradient(135deg, #4557e5, #2d96e8);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  font-weight: 700;
  position: relative;
  padding: 0 2px;
}

.highlight-text::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 100%;
  height: 2px;
  background: linear-gradient(90deg, #4557e5, #2d96e8);
  opacity: 0.6;
  border-radius: 2px;
}

/* 介绍部分 */
.guide-intro {
  margin-bottom: 60px;
}

.intro-text {
  font-size: 16px;
  line-height: 1.8;
  color: var(--text-secondary);
  margin: 16px 0;
}

.steps-container {
  margin: 40px 0;
  padding: 30px;
  background-color: var(--card-bg);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-md);
}

.custom-steps {
  --el-step-icon-size: 32px;
}

/* 提示卡片 */
.tip-card {
  display: flex;
  align-items: flex-start;
  padding: 20px;
  background: linear-gradient(135deg, rgba(69, 87, 229, 0.05), rgba(45, 150, 232, 0.05));
  border-radius: var(--border-radius-md);
  border-left: 4px solid var(--primary-color);
  margin: 30px 0;
}

.tip-icon {
  flex-shrink: 0;
  font-size: 24px;
  color: var(--primary-color);
  margin-right: 16px;
  margin-top: 2px;
}

.tip-text {
  margin: 0;
  line-height: 1.6;
  color: var(--text-secondary);
}

/* 章节通用样式 */
.guide-section {
  margin-bottom: 60px;
  padding-bottom: 40px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

.section-header {
  display: flex;
  align-items: center;
  margin-bottom: 24px;
}

.step-number {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, #4557e5, #2d96e8);
  color: white;
  font-size: 20px;
  font-weight: 700;
  border-radius: 14px;
  margin-right: 16px;
  box-shadow: 0 4px 12px rgba(69, 87, 229, 0.2);
}

.section-title {
  font-size: 24px;
  font-weight: 700;
  margin: 0;
  color: var(--text-primary);
}

.section-text {
  font-size: 16px;
  line-height: 1.8;
  color: var(--text-secondary);
  margin: 16px 0;
}

.conclusion-text {
  margin-top: 1.5rem;
  font-weight: 500;
}

/* 图片容器 */
.image-container {
  margin: 30px 0;
  border-radius: var(--border-radius-md);
  overflow: hidden;
  box-shadow: var(--shadow-md);
  background-color: #f5f7fa;
  padding: 16px;
  text-align: center;
}

.image-container.centered {
  display: flex;
  justify-content: center;
}

.guide-image {
  max-width: 100%;
  height: auto;
  border-radius: var(--border-radius-sm);
}

.guide-image.medium {
  max-width: 60%;
}

/* 数据类型区域 */
.data-types {
  background-color: var(--card-bg);
  border-radius: var(--border-radius-md);
  padding: 24px;
  margin: 24px 0;
  box-shadow: var(--shadow-sm);
  border-left: 4px solid var(--secondary-color);
}

/* 警告卡片 */
.warning-card {
  display: flex;
  align-items: flex-start;
  padding: 20px;
  background: rgba(230, 162, 60, 0.05);
  border-radius: var(--border-radius-md);
  border-left: 4px solid var(--warning-color);
  margin: 30px 0;
}

.warning-icon {
  flex-shrink: 0;
  font-size: 24px;
  color: var(--warning-color);
  margin-right: 16px;
  margin-top: 2px;
}

.warning-text {
  margin: 0;
  line-height: 1.6;
  color: var(--text-secondary);
}

/* 最终部分 */
.final-section {
  border-bottom: none;
}

.final-content {
  background: linear-gradient(135deg, rgba(69, 87, 229, 0.03), rgba(45, 150, 232, 0.03));
  border-radius: var(--border-radius-lg);
  padding: 32px;
  margin-top: 30px;
}

.next-title {
  font-size: 20px;
  font-weight: 700;
  margin: 30px 0 20px;
  color: var(--text-primary);
  background: linear-gradient(135deg, #4557e5, #2d96e8);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.farewell-text {
  font-size: 20px;
  font-weight: 700;
  margin-top: 30px;
  text-align: center;
  color: var(--text-primary);
}

.surprise-text {
  font-weight: 600;
}

.inline-icon {
  width: 20px;
  height: 20px;
  vertical-align: middle;
  margin: 0 4px;
}

/* 标签自定义 */
.custom-tag {
  border-radius: 4px;
  font-weight: 600;
  font-size: 14px;
  padding: 2px 8px;
  margin: 0 4px;
}

.model-tag {
  border-radius: 6px;
  font-weight: 600;
  font-size: 15px;
  padding: 4px 10px;
  margin: 0 4px;
  border: 1px solid rgba(69, 87, 229, 0.2);
  background: rgba(69, 87, 229, 0.05);
  color: var(--primary-color);
}

.model-types-container {
  margin: 40px 0;
  padding: 30px;
  background-color: var(--card-bg);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-md);
}

.model-section-title {
  font-size: 20px;
  font-weight: 700;
  margin: 0 0 24px 0;
  text-align: center;
  color: var(--text-primary);
}

.model-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 24px;
  margin-top: 20px;
}

.model-card {
  background: linear-gradient(135deg, rgba(69, 87, 229, 0.03), rgba(45, 150, 232, 0.03));
  border-radius: var(--border-radius-md);
  padding: 20px;
  border: 1px solid rgba(69, 87, 229, 0.1);
  transition: all 0.3s ease;
}

.model-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-md);
  border-color: rgba(69, 87, 229, 0.2);
}

.model-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.model-rating {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.model-rating-label {
  font-size: 12px;
  color: var(--text-tertiary);
  margin-bottom: 4px;
}

.rating-bars {
  display: flex;
  gap: 2px;
}

.rating-bar {
  width: 16px;
  height: 4px;
  background-color: rgba(69, 87, 229, 0.1);
  border-radius: 2px;
}

.rating-bar.filled {
  background-color: var(--primary-color);
}

.model-description {
  color: var(--text-secondary);
  font-size: 14px;
  line-height: 1.6;
  margin: 0;
}

/* 流程信息 */
.process-info {
  display: flex;
  align-items: flex-start;
  background-color: rgba(69, 87, 229, 0.03);
  border-radius: var(--border-radius-md);
  padding: 24px;
  margin: 30px 0;
  border: 1px solid rgba(69, 87, 229, 0.1);
}

.process-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, rgba(69, 87, 229, 0.1), rgba(45, 150, 232, 0.1));
  border-radius: 50%;
  margin-right: 20px;
  color: var(--primary-color);
  font-size: 20px;
}

.process-title {
  font-size: 18px;
  font-weight: 600;
  margin: 0 0 12px 0;
  color: var(--text-primary);
}

.process-description {
  color: var(--text-secondary);
  margin: 0;
  line-height: 1.6;
}

/* 工作流程 */
.task-workflow {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin: 2rem 0;
  padding: 1.5rem;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.workflow-step {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 28%;
}

.workflow-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 50px;
  height: 50px;
  margin-bottom: 1rem;
  background: linear-gradient(135deg, var(--el-color-primary), var(--el-color-primary-light-3));
  color: white;
  font-size: 1.5rem;
  font-weight: bold;
  border-radius: 50%;
  box-shadow: 0 4px 8px rgba(var(--el-color-primary-rgb), 0.3);
}

.workflow-content {
  text-align: center;
}

.workflow-title {
  margin: 0 0 0.5rem;
  font-size: 1rem;
  font-weight: 600;
  color: var(--el-color-primary-dark-2);
}

.workflow-description {
  margin: 0;
  font-size: 0.9rem;
  color: var(--el-text-color-secondary);
}

.workflow-arrow {
  color: var(--el-color-primary-light-3);
  font-size: 1.5rem;
}

/* 功能卡片 */
.visualization-features {
  margin: 2rem 0;
  padding: 1.5rem;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.feature-section-title {
  text-align: center;
  margin-bottom: 1.5rem;
  font-size: 1.3rem;
  color: var(--el-color-primary-dark-2);
  position: relative;
}

.feature-section-title:after {
  content: '';
  position: absolute;
  bottom: -8px;
  left: 50%;
  transform: translateX(-50%);
  width: 60px;
  height: 3px;
  background: linear-gradient(90deg, var(--el-color-primary), var(--el-color-primary-light-3));
  border-radius: 3px;
}

.feature-cards {
  display: flex;
  justify-content: space-between;
  gap: 1.5rem;
  margin-top: 2rem;
}

.feature-card {
  flex: 1;
  padding: 1.5rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  transition: transform 0.3s, box-shadow 0.3s;
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
}

.feature-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 60px;
  height: 60px;
  margin: 0 auto 1rem;
  background: linear-gradient(135deg, var(--el-color-primary-light-5), var(--el-color-primary-light-8));
  color: var(--el-color-primary);
  font-size: 1.8rem;
  border-radius: 50%;
}

.feature-title {
  margin: 0 0 0.8rem;
  text-align: center;
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--el-color-primary-dark-2);
}

.feature-description {
  margin: 0;
  text-align: center;
  font-size: 0.9rem;
  color: var(--el-text-color-secondary);
  line-height: 1.5;
}

/* 惊喜元素 */
.surprise-container {
  display: flex;
  align-items: center;
  margin-bottom: 24px;
}

.surprise-icon {
  font-size: 24px;
  color: var(--primary-color);
  margin-right: 16px;
}

/* 下一步 */
.next-steps {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin: 30px 0;
}

.next-step {
  display: flex;
  align-items: flex-start;
  padding: 16px;
  background: linear-gradient(135deg, rgba(69, 87, 229, 0.03), rgba(45, 150, 232, 0.03));
  border-radius: var(--border-radius-md);
  border: 1px solid rgba(69, 87, 229, 0.1);
}

.next-step-number {
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 30px;
  height: 30px;
  background: linear-gradient(135deg, #4557e5, #2d96e8);
  color: white;
  font-weight: 600;
  font-size: 14px;
  border-radius: 8px;
  margin-right: 12px;
}

.next-step-text {
  margin: 0;
  line-height: 1.5;
  font-size: 14px;
  color: var(--text-secondary);
}

/* 告别容器 */
.farewell-container {
  text-align: center;
  margin-top: 40px;
  padding-top: 30px;
  border-top: 1px solid rgba(69, 87, 229, 0.1);
}

.support-text {
  font-size: 16px;
  color: var(--text-secondary);
  margin-top: 8px;
}

/* 响应式调整 */
@media screen and (max-width: 768px) {
  .task-workflow {
    flex-direction: column;
    gap: 1.5rem;
  }
  
  .workflow-step {
    width: 100%;
    flex-direction: row;
    text-align: left;
  }
  
  .workflow-icon {
    margin-bottom: 0;
    margin-right: 1rem;
  }
  
  .workflow-content {
    text-align: left;
  }
  
  .workflow-arrow {
    transform: rotate(90deg);
  }
  
  .feature-cards {
    flex-direction: column;
  }
}
</style>