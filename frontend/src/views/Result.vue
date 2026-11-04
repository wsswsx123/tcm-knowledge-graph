<!-- frontend/src/views/Result.vue -->
<template>
  <div class="space-y-6" v-if="result">
    <!-- 医疗免责声明（合规） -->
    <MedicalDisclaimer />
    <div class="flex items-center justify-between mb-4 flex-wrap gap-3">
      <router-link to="/" class="text-primary hover:text-secondary flex items-center font-serif text-lg">
        <ArrowLeft class="w-5 h-5 mr-2" /> 重新辨识
      </router-link>
      <div class="flex items-center gap-2 flex-wrap">
        <!-- 页面顶部：精简视图 / 完整视图 全局切换（同时控制 9 体质推荐 + 主体质 4 大折叠块） -->
        <button
          class="inline-flex items-center px-3 py-1.5 rounded-full border border-primary/40 text-primary hover:bg-primary/5 transition-colors font-serif text-sm shadow-sm"
          @click="expandAllSections"
        >
          <PanelTopOpen class="w-3.5 h-3.5 mr-1" /> 完整视图（展开全部）
        </button>
        <button
          class="inline-flex items-center px-3 py-1.5 rounded-full bg-primary text-paper hover:bg-secondary transition-colors font-serif text-sm shadow-sm"
          @click="collapseAllSections"
        >
          <PanelTopClose class="w-3.5 h-3.5 mr-1" /> 精简视图（折叠全部）
        </button>
        <!-- 跳转多 Agent 页面深入问诊 -->
        <router-link
          :to="`/agent?from_assessment=${result.id}`"
          class="inline-flex items-center px-3 py-1.5 rounded-full bg-white border border-primary/40 text-primary hover:bg-primary hover:text-paper transition-colors font-serif text-sm shadow-sm"
        >
          <ExternalLink class="w-3.5 h-3.5 mr-1" />
          去多 Agent 页面深入问诊
        </router-link>
      </div>
    </div>

    <!-- Result Overview -->
    <div class="bg-white rounded-sm shadow-lg p-8 border border-border text-center relative overflow-hidden">
      <div class="absolute top-0 right-0 opacity-5 text-9xl font-serif -mt-10 -mr-10 pointer-events-none text-primary">
        {{ primaryName[0] }}
      </div>
      <h2 class="text-3xl font-serif font-bold text-secondary mb-3 tracking-widest">辨识结果报告</h2>
      <div class="flex items-center justify-center space-x-4 mb-6">
        <div class="h-[1px] w-12 bg-primary"></div>
        <span class="text-primary font-serif">❖</span>
        <div class="h-[1px] w-12 bg-primary"></div>
      </div>

      <div class="mt-4">
        <p class="text-primary font-serif text-lg tracking-widest mb-2">【 主体质 】</p>
        <p class="text-6xl font-serif font-black text-[#8b3a3a] mb-6 tracking-widest">{{ primaryName }}</p>
        <div class="inline-block bg-paper rounded-sm px-8 py-4 border border-[#c0b298] shadow-inner">
          <p class="text-primary font-serif text-base mb-2">【 兼夹体质 】</p>
          <p class="text-xl font-serif font-medium text-secondary">{{ secondaryNames || '无' }}</p>
        </div>
      </div>
    </div>

    <!-- seed 横幅：已锚定问卷测评 -->
    <div
      v-if="agentChat.seed_source"
      class="flex items-center justify-between flex-wrap gap-2 bg-green-50 border border-green-200 rounded-sm px-4 py-2.5"
    >
      <div class="flex items-center flex-wrap gap-x-3 gap-y-1 text-sm font-serif text-[#2d5016]">
        <CheckCircle2 class="w-4 h-4 text-green-600" />
        <span>
          本次问诊已锚定问卷测评
          <span class="font-bold">#{{ agentChat.seed_source.assessment_id }}</span>
          · 主 <span class="font-bold">{{ agentChat.seed_source.primary_name || primaryName }}</span>
          <template v-if="agentChat.seed_source.secondary_names && agentChat.seed_source.secondary_names.length">
            · 兼夹 <span class="font-bold">{{ agentChat.seed_source.secondary_names.join('、') }}</span>
          </template>
        </span>
      </div>
      <button
        class="text-xs font-serif text-green-800 underline hover:text-green-900"
        :disabled="!isLoggedIn || agentChat.loading"
        @click="askReasonBreakdown"
      >
        查看判定依据
      </button>
    </div>
    <!-- 未登录提示（401 seed 失败时） -->
    <div
      v-if="!isLoggedIn && seed401Hint"
      class="flex items-center justify-between flex-wrap gap-2 bg-amber-50 border border-amber-200 rounded-sm px-4 py-2.5 text-sm font-serif text-amber-800"
    >
      <span><AlertCircle class="w-4 h-4 inline mr-1.5" />登录后即可开启本问卷专属的 AI 养生顾问。</span>
      <router-link to="/auth" class="underline hover:text-amber-900">去登录 →</router-link>
    </div>

    <!-- Charts -->
    <div class="grid md:grid-cols-2 gap-6">
      <div class="bg-white rounded-sm shadow-lg p-4 border border-border">
        <div ref="radarChart" style="height: 380px;"></div>
      </div>
      <div class="bg-white rounded-sm shadow-lg p-4 border border-border">
        <GraphChart v-if="graphData" :data="graphData" style="height: 380px;" />
        <div v-else class="h-full flex items-center justify-center text-[#c0b298] font-serif">暂无图谱数据</div>
      </div>
    </div>

    <!-- 各体质得分占比 -->
    <div class="bg-white rounded-sm shadow-lg p-6 border border-border">
      <h3 class="text-xl font-serif font-bold text-secondary mb-5 flex items-center">
        <TrendingUp class="w-6 h-6 mr-3 text-primary" /> 各体质得分占比
      </h3>
      <div class="space-y-3">
        <div v-for="(score, type) in result.scores" :key="type" class="flex items-center gap-3">
          <div class="w-24 font-serif text-primary">{{ constitutionNames[type] }}</div>
          <div class="flex-1 h-5 bg-gray-200 rounded-full overflow-hidden">
            <div class="h-full bg-primary rounded-full transition-all duration-500"
                 :style="{ width: score + '%' }"></div>
          </div>
          <div class="w-12 text-right font-serif font-medium">{{ score }}%</div>
        </div>
      </div>
    </div>

    <!-- 各体质专属调理方案 -->
    <div v-if="Object.keys(constitutionRecommendations).length" class="bg-white rounded-sm shadow-lg p-6 border border-border">
      <div class="flex items-center justify-between mb-5">
        <h3 class="text-xl font-serif font-bold text-secondary flex items-center">
          <Layers class="w-6 h-6 mr-3 text-primary" /> 各体质专属调理方案
          <span class="ml-3 text-sm font-normal text-[#8b7355]">
            （共 {{ Object.keys(constitutionRecommendations).length }} 种，可单独折叠）
          </span>
        </h3>
        <div class="flex items-center gap-2 flex-shrink-0">
          <button
            class="inline-flex items-center px-3 py-1.5 rounded border border-primary/30 text-primary text-sm font-serif hover:bg-primary/5 transition-colors"
            @click="expandAllConstitutionRecs"
          ><ChevronsDown class="w-4 h-4 mr-1" /> 全部展开</button>
          <button
            class="inline-flex items-center px-3 py-1.5 rounded border border-primary/30 text-primary text-sm font-serif hover:bg-primary/5 transition-colors"
            @click="collapseAllConstitutionRecs"
          ><ChevronsUp class="w-4 h-4 mr-1" /> 全部折叠</button>
        </div>
      </div>

      <div
        v-for="(rec, type) in constitutionRecommendations"
        :key="type"
        class="mb-3 last:mb-0 border border-border rounded-sm overflow-hidden"
        :class="constitutionSectionOpen[type] ? '' : 'border-b border-l border-r'"
      >
        <!-- 折叠标题头 -->
        <button
          type="button"
          class="w-full px-4 py-3 flex items-center justify-between bg-paper hover:bg-paper/80 transition-colors border-b"
          :class="constitutionSectionOpen[type] ? 'border-b border-border' : 'border-b-0'"
          @click="toggleConstitutionSection(type)"
        >
          <div class="flex items-center gap-3">
            <component :is="constitutionSectionOpen[type] ? ChevronDown : ChevronRight" class="w-4 h-4 text-primary flex-shrink-0" />
            <div class="text-left">
              <div class="flex items-center gap-2 flex-wrap">
                <h4 class="text-lg font-serif font-bold text-primary">{{ constitutionNames[type] }}</h4>
                <span
                  v-if="type === result.primary"
                  class="text-xs px-2 py-0.5 rounded bg-[#8b3a3a] text-paper font-serif"
                >主体质</span>
                <span
                  v-else-if="(result.scores?.[type] ?? 0) >= 40"
                  class="text-xs px-2 py-0.5 rounded bg-amber-100 text-amber-800 border border-amber-200 font-serif"
                >兼夹（命中≥40）</span>
                <span
                  v-else
                  class="text-xs px-2 py-0.5 rounded bg-gray-100 text-gray-600 border border-gray-200 font-serif"
                >倾向（30≤分<40）</span>
              </div>
              <p class="text-sm text-gray-500 mt-1">得分：{{ result.scores?.[type] ?? '--' }}%</p>
            </div>
          </div>
          <span class="text-xs font-serif text-[#8b7355] mr-2 flex-shrink-0">
            {{ constitutionSectionOpen[type] ? '点击收起 ↑' : '点击展开 ↓' }}
          </span>
        </button>

        <!-- 折叠内容区 -->
        <div v-show="constitutionSectionOpen[type]" class="p-4 bg-white">
          <div class="grid md:grid-cols-3 gap-5">
            <!-- 穴位 -->
            <div v-if="rec.acupoints?.length">
              <h5 class="font-serif font-semibold text-secondary mb-2 flex items-center"><Wind class="w-4 h-4 mr-1" /> 穴位推荐</h5>
              <ul class="space-y-2 text-sm">
                <li v-for="a in rec.acupoints.slice(0, 3)" :key="a.name">
                  <span class="font-bold">{{ a.name }}</span>：{{ a.location }}
                </li>
              </ul>
            </div>
            <!-- 食疗 -->
            <div v-if="rec.foods?.length">
              <h5 class="font-serif font-semibold text-secondary mb-2 flex items-center"><Apple class="w-4 h-4 mr-1" /> 食疗推荐</h5>
              <ul class="space-y-2 text-sm">
                <li v-for="f in rec.foods.slice(0,3)" :key="f.name">
                  <span class="font-bold">{{ f.name }}</span>：{{ f.effect }}
                </li>
              </ul>
            </div>
            <!-- 运动 -->
            <div v-if="rec.exercises?.length">
              <h5 class="font-serif font-semibold text-secondary mb-2 flex items-center"><Activity class="w-4 h-4 mr-1" /> 运动推荐</h5>
              <ul class="space-y-2 text-sm">
                <li v-for="e in rec.exercises.slice(0,3)" :key="e.name">
                  <span class="font-bold">{{ e.name }}</span>：{{ e.method }}
                </li>
              </ul>
            </div>
          </div>
          <div v-if="!rec.acupoints?.length && !rec.foods?.length && !rec.exercises?.length"
               class="text-center text-[#c0b298] italic text-sm py-3">
            该体质暂无专属调理推荐
          </div>
        </div>
      </div>
    </div>

    <!-- 原有专属调理方案（主体质增强推荐） -->
    <div v-if="recommendations" class="bg-white rounded-sm shadow-lg p-6 border border-border">
      <div class="flex items-center justify-between flex-wrap gap-3 mb-5">
        <h3 class="text-xl font-serif font-bold text-secondary flex items-center tracking-widest">
          <span class="text-primary mr-3">❖</span> 您的专属调理方案 <span class="text-primary ml-3">❖</span>
        </h3>
        <div class="flex items-center gap-2 flex-shrink-0">
          <button
            class="inline-flex items-center px-3 py-1.5 rounded border border-secondary/50 text-secondary text-sm font-serif hover:bg-[#8b3a3a]/5 transition-colors"
            @click="expandAllMainSections"
          ><ChevronsDown class="w-4 h-4 mr-1" /> 展开全部</button>
          <button
            class="inline-flex items-center px-3 py-1.5 rounded border border-secondary/50 text-secondary text-sm font-serif hover:bg-[#8b3a3a]/5 transition-colors"
            @click="collapseAllMainSections"
          ><ChevronsUp class="w-4 h-4 mr-1" /> 折叠全部</button>
          <span class="h-5 w-px bg-border mx-1 hidden sm:block"></span>
          <button
            class="inline-flex items-center px-3 py-1.5 rounded bg-primary text-paper text-sm font-serif hover:bg-secondary transition-colors shadow-sm"
            @click="toggleMainCompactView"
          >
            <component :is="isMainCompactView ? Maximize2 : Minimize2" class="w-4 h-4 mr-1" />
            {{ isMainCompactView ? '切换完整视图' : '切换精简视图' }}
          </button>
        </div>
      </div>

      <!-- 第1折叠块：经络穴位 + 药膳食疗 + 运动 三合一 -->
      <div class="border border-border rounded-sm overflow-hidden mb-4">
        <button
          type="button"
          class="w-full px-4 py-3 flex items-center justify-between bg-paper/60 hover:bg-paper transition-colors"
          :class="mainSectionOpen.trio ? 'border-b border-border' : 'border-b-0'"
          @click="toggleMainSection('trio')"
        >
          <div class="flex items-center gap-3">
            <component :is="mainSectionOpen.trio ? ChevronDown : ChevronRight" class="w-5 h-5 text-[#8b3a3a] flex-shrink-0" />
            <div>
              <h4 class="text-lg font-serif font-bold text-[#8b3a3a] flex items-center flex-wrap gap-4">
                <span class="inline-flex items-center"><Wind class="w-5 h-5 mr-1" /> 经络穴位调理</span>
                <span class="text-[#8b7355] font-serif">/</span>
                <span class="inline-flex items-center"><Apple class="w-5 h-5 mr-1" /> 药膳食疗推荐</span>
                <span class="text-[#8b7355] font-serif">/</span>
                <span class="inline-flex items-center"><Activity class="w-5 h-5 mr-1" /> 运动方案推荐</span>
              </h4>
              <p class="text-xs text-[#8b7355] mt-1 font-serif">
                {{ countMainRecommendations('acupoints') }} 个穴位 ·
                {{ countMainRecommendations('foods') }} 个食疗 ·
                {{ countMainRecommendations('exercises') }} 个运动
              </p>
            </div>
          </div>
          <span class="text-xs font-serif text-[#8b7355] mr-2 flex-shrink-0">
            {{ mainSectionOpen.trio ? '收起 ↑' : '展开 ↓' }}
          </span>
        </button>

        <div v-show="mainSectionOpen.trio">
          <div class="grid md:grid-cols-3 gap-8 p-6">
            <!-- Acupoints -->
            <div>
              <h4 class="text-lg font-serif font-bold text-primary mb-4 flex items-center border-b-2 border-border pb-2">
                <Wind class="w-5 h-5 mr-2" /> 经络穴位调理
              </h4>
              <div class="space-y-4">
                <div
                  v-for="(a,i) in recommendations.acupoints"
                  :key="i"
                  class="bg-paper rounded-sm p-4 border-l-4 border-[#b8860b] shadow-sm relative"
                >
                  <p class="font-serif font-bold text-secondary text-lg mb-1">{{ a.name }}</p>
                  <p class="text-sm text-[#6b5c51] mb-1"><span class="font-semibold text-primary">取穴：</span>{{ a.location }}</p>
                  <p class="text-sm text-[#6b5c51] mb-1"><span class="font-semibold text-primary">方法：</span>{{ a.method }}</p>
                  <p v-if="a.reason" class="text-xs text-amber-700 mt-2 bg-amber-50 p-2 rounded pr-16">
                    <span class="font-semibold">✨ 小贴士：</span>{{ a.reason }}
                  </p>
                  <button
                    class="absolute bottom-2 right-2 inline-flex items-center px-2 py-0.5 rounded border border-primary/30 bg-white/80 backdrop-blur hover:text-secondary transition-colors shadow-sm"
                    :disabled="!isLoggedIn || agentChat.loading"
                    :class="isLoggedIn ? 'text-primary' : 'text-[#c0b298] cursor-not-allowed'"
                    @click="askAcupoint(a)"
                  >
                    <MessageSquare class="w-3.5 h-3.5 mr-1" />
                    <span class="text-xs font-serif">问 AI</span>
                  </button>
                </div>
                <p v-if="!recommendations.acupoints?.length" class="text-[#c0b298] italic text-sm">暂无穴位推荐</p>
              </div>
            </div>
            <!-- Foods -->
            <div>
              <h4 class="text-lg font-serif font-bold text-primary mb-4 flex items-center border-b-2 border-border pb-2">
                <Apple class="w-5 h-5 mr-2" /> 药膳食疗推荐
              </h4>
              <div class="space-y-4">
                <div
                  v-for="(f,i) in recommendations.foods"
                  :key="i"
                  class="bg-paper rounded-sm p-4 border-l-4 border-[#556b2f] shadow-sm relative"
                >
                  <p class="font-serif font-bold text-secondary text-lg mb-1">{{ f.name }}</p>
                  <p class="text-sm text-[#6b5c51] mb-1"><span class="font-semibold text-primary">性味：</span>{{ f.nature }}</p>
                  <p class="text-sm text-[#6b5c51] mb-1"><span class="font-semibold text-primary">功效：</span>{{ f.effect }}</p>
                  <p v-if="f.reason" class="text-xs text-amber-700 mt-2 bg-amber-50 p-2 rounded pr-16">
                    <span class="font-semibold">✨ 小贴士：</span>{{ f.reason }}
                  </p>
                  <button
                    class="absolute bottom-2 right-2 inline-flex items-center px-2 py-0.5 rounded border border-primary/30 bg-white/80 backdrop-blur hover:text-secondary transition-colors shadow-sm"
                    :disabled="!isLoggedIn || agentChat.loading"
                    :class="isLoggedIn ? 'text-primary' : 'text-[#c0b298] cursor-not-allowed'"
                    @click="askFood(f)"
                  >
                    <MessageSquare class="w-3.5 h-3.5 mr-1" />
                    <span class="text-xs font-serif">问 AI</span>
                  </button>
                </div>
                <p v-if="!recommendations.foods?.length" class="text-[#c0b298] italic text-sm">暂无食疗推荐</p>
              </div>
            </div>
            <!-- Exercises -->
            <div>
              <h4 class="text-lg font-serif font-bold text-primary mb-4 flex items-center border-b-2 border-border pb-2">
                <Activity class="w-5 h-5 mr-2" /> 运动方案推荐
              </h4>
              <div class="space-y-4">
                <div
                  v-for="(e,i) in recommendations.exercises"
                  :key="i"
                  class="bg-paper rounded-sm p-4 border-l-4 border-[#4682b4] shadow-sm relative"
                >
                  <p class="font-serif font-bold text-secondary text-lg mb-1">{{ e.name }}</p>
                  <p class="text-sm text-[#6b5c51] mb-1"><span class="font-semibold text-primary">功效：</span>{{ e.effect }}</p>
                  <p class="text-sm text-[#6b5c51] mb-1"><span class="font-semibold text-primary">方法：</span>{{ e.method }}</p>
                  <p v-if="e.reason" class="text-xs text-amber-700 mt-2 bg-amber-50 p-2 rounded pr-16">
                    <span class="font-semibold">✨ 小贴士：</span>{{ e.reason }}
                  </p>
                  <button
                    class="absolute bottom-2 right-2 inline-flex items-center px-2 py-0.5 rounded border border-primary/30 bg-white/80 backdrop-blur hover:text-secondary transition-colors shadow-sm"
                    :disabled="!isLoggedIn || agentChat.loading"
                    :class="isLoggedIn ? 'text-primary' : 'text-[#c0b298] cursor-not-allowed'"
                    @click="askExercise(e)"
                  >
                    <MessageSquare class="w-3.5 h-3.5 mr-1" />
                    <span class="text-xs font-serif">问 AI</span>
                  </button>
                </div>
                <p v-if="!recommendations.exercises?.length" class="text-[#c0b298] italic text-sm">暂无运动推荐</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 第2折叠块：专属疗法过程 -->
      <div
        v-if="recommendations.therapy_process?.length"
        class="border border-border rounded-sm overflow-hidden mb-4"
      >
        <button
          type="button"
          class="w-full px-4 py-3 flex items-center justify-between bg-paper/60 hover:bg-paper transition-colors"
          :class="mainSectionOpen.therapy ? 'border-b border-border' : 'border-b-0'"
          @click="toggleMainSection('therapy')"
        >
          <div class="flex items-center gap-3">
            <component :is="mainSectionOpen.therapy ? ChevronDown : ChevronRight" class="w-5 h-5 text-[#2e8b57] flex-shrink-0" />
            <div>
              <h4 class="text-lg font-serif font-bold text-primary flex items-center">
                <Sparkles class="w-5 h-5 mr-2" /> 专属疗法过程
              </h4>
              <p class="text-xs text-[#8b7355] mt-1 font-serif">共 {{ recommendations.therapy_process.length }} 个步骤</p>
            </div>
          </div>
          <span class="text-xs font-serif text-[#8b7355] mr-2 flex-shrink-0">
            {{ mainSectionOpen.therapy ? '收起 ↑' : '展开 ↓' }}
          </span>
        </button>
        <div v-show="mainSectionOpen.therapy" class="p-6">
          <div class="space-y-4">
            <div
              v-for="(tp, i) in recommendations.therapy_process"
              :key="i"
              class="bg-paper rounded-sm p-4 border-l-4 border-[#2e8b57] shadow-sm relative"
            >
              <p class="font-serif font-bold text-secondary text-lg mb-1">{{ tp.name }}</p>
              <p class="text-sm text-[#6b5c51] mb-1"><span class="font-semibold text-primary">基础：</span>{{ tp.base }}</p>
              <p class="text-sm text-[#6b5c51] mb-1"><span class="font-semibold text-primary">顺序：</span>{{ tp.sequence }}</p>
              <p class="text-sm text-[#6b5c51] mb-1"><span class="font-semibold text-primary">频率：</span>{{ tp.frequency }}</p>
              <p v-if="tp.reason" class="text-xs text-amber-700 mt-2 bg-amber-50 p-2 rounded pr-16">
                <span class="font-semibold">✨ 小贴士：</span>{{ tp.reason }}
              </p>
              <button
                class="absolute bottom-2 right-2 inline-flex items-center px-2 py-0.5 rounded border border-primary/30 bg-white/80 backdrop-blur hover:text-secondary transition-colors shadow-sm"
                :disabled="!isLoggedIn || agentChat.loading"
                :class="isLoggedIn ? 'text-primary' : 'text-[#c0b298] cursor-not-allowed'"
                @click="askTherapy(tp)"
              >
                <MessageSquare class="w-3.5 h-3.5 mr-1" />
                <span class="text-xs font-serif">问 AI</span>
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- 第3折叠块：养生知识 -->
      <div
        v-if="recommendations.health_knowledge?.length"
        class="border border-border rounded-sm overflow-hidden mb-4"
      >
        <button
          type="button"
          class="w-full px-4 py-3 flex items-center justify-between bg-paper/60 hover:bg-paper transition-colors"
          :class="mainSectionOpen.health ? 'border-b border-border' : 'border-b-0'"
          @click="toggleMainSection('health')"
        >
          <div class="flex items-center gap-3">
            <component :is="mainSectionOpen.health ? ChevronDown : ChevronRight" class="w-5 h-5 text-[#8b7355] flex-shrink-0" />
            <div>
              <h4 class="text-lg font-serif font-bold text-primary flex items-center">
                <BookOpen class="w-5 h-5 mr-2" /> 养生知识
              </h4>
              <p class="text-xs text-[#8b7355] mt-1 font-serif">共 {{ recommendations.health_knowledge.length }} 条科普</p>
            </div>
          </div>
          <span class="text-xs font-serif text-[#8b7355] mr-2 flex-shrink-0">
            {{ mainSectionOpen.health ? '收起 ↑' : '展开 ↓' }}
          </span>
        </button>
        <div v-show="mainSectionOpen.health" class="p-6">
          <div class="grid md:grid-cols-2 gap-4">
            <div
              v-for="(hk, i) in recommendations.health_knowledge"
              :key="i"
              class="bg-paper rounded-sm p-4 border border-[#c0b298] shadow-sm relative"
            >
              <p class="font-serif font-bold text-secondary text-base mb-1 pr-12">{{ hk.category }}</p>
              <p class="text-sm text-[#6b5c51] pr-16">{{ hk.content }}</p>
              <p v-if="hk.reason" class="text-xs text-amber-700 mt-2 bg-amber-50 p-2 rounded pr-16">
                <span class="font-semibold">💡 建议：</span>{{ hk.reason }}
              </p>
              <button
                class="absolute bottom-2 right-2 inline-flex items-center px-2 py-0.5 rounded border border-primary/30 bg-white/80 backdrop-blur hover:text-secondary transition-colors shadow-sm"
                :disabled="!isLoggedIn || agentChat.loading"
                :class="isLoggedIn ? 'text-primary' : 'text-[#c0b298] cursor-not-allowed'"
                @click="askHealthKnowledge(hk)"
              >
                <MessageSquare class="w-3.5 h-3.5 mr-1" />
                <span class="text-xs font-serif">问 AI</span>
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- 第4折叠块：注意事项（温馨提示） -->
      <div
        v-if="recommendations.precautions?.length"
        class="border border-amber-200 rounded-sm overflow-hidden"
      >
        <button
          type="button"
          class="w-full px-4 py-3 flex items-center justify-between bg-amber-50 hover:bg-amber-50/80 transition-colors"
          :class="mainSectionOpen.precautions ? 'border-b border-amber-200' : 'border-b-0'"
          @click="toggleMainSection('precautions')"
        >
          <div class="flex items-center gap-3">
            <component :is="mainSectionOpen.precautions ? ChevronDown : ChevronRight" class="w-5 h-5 text-amber-600 flex-shrink-0" />
            <div>
              <h5 class="text-base font-serif font-bold text-amber-800 flex items-center">
                <span class="w-1 h-5 bg-amber-500 mr-2"></span> 温馨提示（注意事项）
              </h5>
              <p class="text-xs text-amber-700 mt-1 font-serif">共 {{ recommendations.precautions.length }} 条</p>
            </div>
          </div>
          <span class="text-xs font-serif text-amber-700 mr-2 flex-shrink-0">
            {{ mainSectionOpen.precautions ? '收起 ↑' : '展开 ↓' }}
          </span>
        </button>
        <div v-show="mainSectionOpen.precautions" class="p-5 bg-amber-50/50">
          <ul class="list-disc list-inside space-y-2 text-sm">
            <li
              v-for="(item, idx) in recommendations.precautions"
              :key="idx"
              class="text-amber-800 flex items-start gap-2"
            >
              <span class="flex-1">{{ item }}</span>
              <button
                class="inline-flex items-center px-2 py-0.5 rounded border border-primary/30 bg-white/80 backdrop-blur hover:text-secondary transition-colors shadow-sm flex-shrink-0"
                :disabled="!isLoggedIn || agentChat.loading"
                :class="isLoggedIn ? 'text-primary' : 'text-[#c0b298] cursor-not-allowed'"
                @click="askPrecaution(item)"
              >
                <MessageSquare class="w-3.5 h-3.5 mr-1" />
                <span class="text-xs font-serif">问 AI</span>
              </button>
            </li>
          </ul>
        </div>
      </div>
    </div>

    <!-- 专属养生顾问卡片（嵌入 mini 版聊天面板） -->
    <div class="bg-white rounded-sm shadow-lg border border-border overflow-hidden">
      <div class="bg-primary/10 border-b border-border px-5 py-3 flex items-center justify-between">
        <h3 class="text-lg font-serif font-bold text-secondary flex items-center">
          <Bot class="w-5 h-5 mr-2 text-primary" /> 🤖 专属养生顾问
          <span class="ml-2 text-xs font-serif text-[#8b7355] font-normal">（基于本次问卷结果，不用重复做症状辨识）</span>
        </h3>
        <span
          v-if="agentChat.loading"
          class="inline-flex items-center text-xs font-serif text-primary"
        >
          <Loader2 class="w-3.5 h-3.5 mr-1 animate-spin" /> AI 思考中...
        </span>
      </div>
      <div class="relative h-[70vh] max-h-[800px] min-h-[400px] w-full">
        <!-- 未登录遮罩 -->
        <div
          v-if="!isLoggedIn"
          class="absolute inset-0 z-10 bg-white/80 backdrop-blur-sm flex flex-col items-center justify-center px-8 text-center"
        >
          <Bot class="w-14 h-14 mb-4 text-primary/30" />
          <p class="font-serif text-[#6b5c51] text-base max-w-md leading-relaxed">
            登录后即可在本页直接追问推荐项的细节（为什么推荐、禁忌、频率、调整等），AI 将基于本次问卷结果精准回答，不再重复做症状辨识。
          </p>
          <router-link
            to="/auth"
            class="mt-5 inline-flex items-center px-5 py-2 rounded bg-primary text-paper hover:bg-secondary transition-colors font-serif text-sm shadow"
          >
            <LogIn class="w-4 h-4 mr-2" /> 立即登录
          </router-link>
        </div>
        <AgentChatPanel
          ref="panelRef"
          mode="mini"
          :skipRestore="hasAutoSeeded"
          @seeded="onSeeded"
          @error="onPanelError"
          @session-changed="onSessionChanged"
        />
      </div>
      <!-- mini 模式 toast：Result.vue 自己的提示（seed 失败等） -->
      <div
        v-if="panelToast"
        class="px-5 py-2 bg-amber-50 border-t border-amber-200 text-xs font-serif text-amber-900 flex items-center"
      >
        <AlertTriangle class="w-3.5 h-3.5 mr-2 flex-shrink-0 text-amber-600" />
        <span class="flex-1">{{ panelToast }}</span>
        <button
          class="ml-2 text-amber-600 hover:text-amber-800"
          @click="panelToast = ''"
        >
          <XCircle class="w-3.5 h-3.5" />
        </button>
      </div>
    </div>
  </div>
  <div v-else-if="loading" class="text-center py-10 text-primary">正在分析您的体质数据...</div>
  <div v-else class="text-center py-10 text-red-500">未找到测评结果</div>
</template>

<script setup>
import { ref, reactive, onMounted, onUnmounted, nextTick, computed, watch } from 'vue'
import { useRoute } from 'vue-router'
import echarts from '@/utils/echarts'
import GraphChart from '@/components/GraphChart.vue'
import AgentChatPanel from '@/components/AgentChatPanel.vue'
import MedicalDisclaimer from '@/components/MedicalDisclaimer.vue'
import { useAgentChatStore } from '@/store/agentChat'
import {
  ArrowLeft,
  Wind,
  Apple,
  Activity,
  Sparkles,
  BookOpen,
  TrendingUp,
  Layers,
  MessageSquare,
  ExternalLink,
  CheckCircle2,
  AlertCircle,
  AlertTriangle,
  XCircle,
  Bot,
  Loader2,
  LogIn,
  ChevronDown,
  ChevronRight,
  ChevronsDown,
  ChevronsUp,
  Minimize2,
  Maximize2,
  PanelTopClose,
  PanelTopOpen,
} from 'lucide-vue-next'
import axios from '@/api'

const route = useRoute()
const result = ref(null)
const graphData = ref(null)
const recommendations = ref(null)
const loading = ref(true)
const radarChart = ref(null)
const constitutionRecommendations = ref({})

// 【折叠状态①】各体质专属调理方案：按体质 key 存 true/false
const constitutionSectionOpen = reactive({})
// 【折叠状态②】主体质专属调理方案：4 大折叠块开关 + 精简视图模式
const mainSectionOpen = reactive({
  trio: true,        // 经络/食疗/运动三合一 默认展开
  therapy: true,     // 疗法过程 默认展开
  health: true,      // 养生知识 默认展开
  precautions: true, // 温馨注意事项 默认展开
})
const isMainCompactView = ref(false) // 是否「精简视图」（一键收起全部）

const agentChat = useAgentChatStore()
const panelRef = ref(null)
const hasAutoSeeded = ref(false)
const seed401Hint = ref(false)
const panelToast = ref('')

const constitutionNames = {
  pinghe: '平和质',
  qixu: '气虚质',
  yangxu: '阳虚质',
  yinxu: '阴虚质',
  tanshi: '痰湿质',
  shire: '湿热质',
  xueyu: '血瘀质',
  qiyu: '气郁质',
  tebing: '特禀质',
}

const isLoggedIn = computed(() => {
  try {
    return Boolean(localStorage.getItem('tcm_user'))
  } catch (e) {
    return false
  }
})

const primaryName = computed(() => constitutionNames[result.value?.primary] || '未知体质')
const secondaryNames = computed(
  () => (result.value?.secondary || []).map((s) => constitutionNames[s]).join('、') || ''
)

const secondaryNamesForPrompt = computed(() => secondaryNames.value)

// ------------------- 折叠交互（各体质专属调理方案） -------------------
// 数据到达后初始化每个体质的默认展开状态：主体质 & 得分≥40(兼夹) 默认展开；
// 倾向(30~40) 默认折叠，避免页面过长。
const initConstitutionSections = () => {
  const types = Object.keys(constitutionRecommendations.value || {})
  if (!types.length) return
  const primaryKey = result.value?.primary
  const scores = result.value?.scores || {}
  types.forEach((t) => {
    if (t === primaryKey) {
      constitutionSectionOpen[t] = true
    } else if ((scores[t] ?? 0) >= 40) {
      constitutionSectionOpen[t] = true
    } else {
      constitutionSectionOpen[t] = false
    }
  })
}
const toggleConstitutionSection = (type) => {
  constitutionSectionOpen[type] = !constitutionSectionOpen[type]
}
const expandAllConstitutionRecs = () => {
  Object.keys(constitutionRecommendations.value || {}).forEach((t) => {
    constitutionSectionOpen[t] = true
  })
}
const collapseAllConstitutionRecs = () => {
  Object.keys(constitutionRecommendations.value || {}).forEach((t) => {
    constitutionSectionOpen[t] = false
  })
}

// ------------------- 折叠交互（主体质专属调理方案） -------------------
const MAIN_SECTION_KEYS = ['trio', 'therapy', 'health', 'precautions']
const toggleMainSection = (key) => {
  if (!MAIN_SECTION_KEYS.includes(key)) return
  mainSectionOpen[key] = !mainSectionOpen[key]
}
const expandAllMainSections = () => {
  MAIN_SECTION_KEYS.forEach((k) => (mainSectionOpen[k] = true))
  isMainCompactView.value = false
}
const collapseAllMainSections = () => {
  MAIN_SECTION_KEYS.forEach((k) => (mainSectionOpen[k] = false))
  isMainCompactView.value = true
}
const toggleMainCompactView = () => {
  if (isMainCompactView.value) {
    // 精简→完整：恢复默认「全展开」
    expandAllMainSections()
  } else {
    collapseAllMainSections()
  }
}
const countMainRecommendations = (key) => {
  const arr = recommendations.value?.[key]
  return Array.isArray(arr) ? arr.length : 0
}

// ------------------- 顶部全局：精简视图 / 完整视图 -------------------
// 一次性展开/折叠 9 体质专属推荐 + 主体质 4 大折叠块
const expandAllSections = () => {
  expandAllConstitutionRecs()
  expandAllMainSections()
}
const collapseAllSections = () => {
  collapseAllConstitutionRecs()
  collapseAllMainSections()
}

// 自动 seed
onMounted(async () => {
  // 尽早安装：后续 store.sendMessage 调用（无论用户自由输入 / 6 个按钮）
  // 都会自动注入页面上已经加载好的调理方案前缀。
  _installStoreSendWrapper()
  try {
    const id = route.params.id
    const resResult = await axios.get(`/api/assessment/${id}`)
    result.value = resResult.data

    // 获取所有体质的推荐方案（用于各体质专属方案）
    if (result.value && result.value.scores) {
      await fetchAllConstitutionRecommendations(result.value.scores)
      // 推荐全加载完后再初始化折叠状态
      initConstitutionSections()
    }

    // 使用增强推荐（主体质）
    if (resResult.data.enhanced_recommendations) {
      recommendations.value = resResult.data.enhanced_recommendations
    } else if (result.value.primary) {
      const resRec = await axios.get(`/api/recommend/${result.value.primary}`)
      recommendations.value = resRec.data
    }

    if (result.value.primary) {
      const resGraph = await axios.get(`/api/graph/${result.value.primary}`)
      graphData.value = resGraph.data
    }

    await nextTick()
    initRadarChart()

    // 自动 seed：仅当用户已登录 & 还没 seed 过同一份
    if (result.value && result.value.id && isLoggedIn.value) {
      const aid = Number(result.value.id)
      if (
        agentChat.seed_source &&
        Number(agentChat.seed_source.assessment_id) === aid
      ) {
        hasAutoSeeded.value = true
      } else {
        try {
          await agentChat.seedFromAssessment(aid)
          hasAutoSeeded.value = true
        } catch (err) {
          const status = err && err.status
          if (status === 401) seed401Hint.value = true
          onPanelError(
            (err && err.userMessage) || (err && err.message) || '导入问卷测评失败',
            status || (err && err.code) || 'seed_error'
          )
        }
      }
    } else if (!isLoggedIn.value) {
      seed401Hint.value = true
    }
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
})

// 未登录 -> 登录状态变化 时，重置 seed401Hint 自动消失
watch(isLoggedIn, (v) => {
  if (v) seed401Hint.value = false
})

// 获取所有体质的推荐方案
const fetchAllConstitutionRecommendations = async (scores) => {
  const promises = Object.keys(scores).map(async (type) => {
    try {
      const res = await axios.get(`/api/recommend/${type}`)
      return { type, data: res.data }
    } catch (err) {
      console.error(`获取${type}推荐失败:`, err)
      return { type, data: null }
    }
  })
  const results = await Promise.all(promises)
  const recMap = {}
  results.forEach((r) => {
    if (r.data) recMap[r.type] = r.data
  })
  constitutionRecommendations.value = recMap
}

const onSeeded = (seedSource) => {
  console.info('[Result] panel seeded:', seedSource)
  hasAutoSeeded.value = true
  seed401Hint.value = false
}
const onPanelError = (message, code) => {
  panelToast.value = message || '出错了'
  setTimeout(() => {
    if (panelToast.value === (message || '出错了')) panelToast.value = ''
  }, 4500)
}
const onSessionChanged = (sid) => {
  console.info('[Result] session changed:', sid)
}

// ============================================================
// 【核心：自动把页面上已经加载好的「专属调理方案」作为 ground truth
//   注入 Agent 对话前缀，避免用户再去翻页面找推荐】
// 遵循 Experience 2126970：不要让用户再提供页面上已经有的信息。
// ============================================================

/** 意图关键字 → 对应调理方案字段 */
const _INTENT_PATTERNS = {
  foods: [
    '吃什么', '吃啥', '食疗', '饮食', '药膳', '食谱', '菜单', '忌口', '禁吃',
    '食物', '食材', '煲汤', '搭配', '营养', '性味', '餐', '补什么', '泡茶', '喝什么'
  ],
  acupoints: [
    '穴位', '按什么', '按哪', '按摩', '经络', '推拿', '针灸', '艾灸', '拔罐', '刮痧',
    '穴位推荐', '按揉', '按压', '点穴'
  ],
  exercises: [
    '怎么做运动', '做什么运动', '运动', '锻炼', '八段锦', '太极', '散步', '跑步',
    '拉伸', '瑜伽', '功法', '呼吸', '健身', '怎么练', '体育'
  ],
  therapy_process: [
    '疗法', '疗程', '治疗方案', '调理流程', '调理步骤', '做多少次', '频率',
    '顺序', '怎么操作', '如何调理', '具体步骤'
  ],
  precautions: [
    '注意事项', '不能吃', '要注意', '禁忌', '什么不能', '不能做', '禁止',
    '什么避免', '避免', '小心', '慎用', '什么不该'
  ],
  health_knowledge: [
    '养生', '科普', '知识', '健康常识', '怎么养生', '生活习惯', '作息',
    '季节养生', '起居', '保养', '养护'
  ],
}
/** 总方案意图：一般问『怎么办 / 给我方案 / 我该做什么』——全部字段都带上 */
const _GENERAL_INTENT = [
  '怎么办', '怎么调', '调理方案', '给我方案', '推荐方案', '我该做什么',
  '我应该怎么', '整体方案', '综述', '总结', '给我建议', '该怎么办', '怎么做',
  '给方案', '全部推荐', '完整推荐', '你给我说说'
]
/** 小寒暄/闲聊：不附加 ground truth 前缀（减少 token 浪费） */
const _CHATTER_PATTERNS = [
  '你好', '您好', 'hi', 'hello', '在吗', '在不在', '在么', '再见', '谢谢',
  '感谢', '多谢', '嗯嗯', '嗯', '好的', '好嘞', 'ok', 'OK', '明白了', '收到',
  '哈哈哈', '哈哈', '对', '是的', '好啊', '行'
]

function _detectIntents(text) {
  if (!text) return new Set()
  const normalized = String(text).toLowerCase()
  // Chatter first
  for (const p of _CHATTER_PATTERNS) {
    if (normalized === p.toLowerCase() || normalized.startsWith(p.toLowerCase() + ' ') || normalized.startsWith(p.toLowerCase() + '，') || normalized.startsWith(p.toLowerCase() + ',')) {
      return new Set(['__chatter__'])
    }
  }
  const found = new Set()
  for (const [field, patterns] of Object.entries(_INTENT_PATTERNS)) {
    for (const p of patterns) {
      if (normalized.includes(p)) { found.add(field); break }
    }
  }
  for (const p of _GENERAL_INTENT) {
    if (normalized.includes(p)) {
      // 带上全部 6 类
      found.add('foods'); found.add('acupoints'); found.add('exercises')
      found.add('therapy_process'); found.add('precautions'); found.add('health_knowledge')
      break
    }
  }
  return found
}

function _joinAry(arr, fn, limit = 4) {
  if (!Array.isArray(arr) || !arr.length) return ''
  return arr.slice(0, limit).map(fn).filter(Boolean).join('；')
}

/**
 * 根据意图把 recommendations（主体质）+ constitutionRecommendations（兼夹≥40）
 * 精简拼接成 ground truth 前缀文本。
 * 输出控制在 ~600 字内，避免超出 1000 字符后端限制。
 */
function _buildPlanPrefix(intents, { recommendations: recs, constitutionRecs, result: r }) {
  if (!recs && !constitutionRecs) return ''
  const primaryNameStr = primaryName.value
  const primaryKey = r?.primary
  const scores = r?.scores || {}
  const secKeys = (r?.secondary || []).slice(0, 2)

  const lines = []
  lines.push(`【系统已附加本次问卷辨识的【专属调理方案】(主体质：${primaryNameStr})。请严格以下面列出的内容为主回答用户，不要编造未列出的穴位/食材/运动/注意事项；如需解释只需对现有条目展开，不要新增。】`)

  // 主体质部分
  lines.push(`【主体质「${primaryNameStr}」专属调理方案】`)
  const has = (k) => Array.isArray(recs?.[k]) && recs[k].length > 0
  if (intents.has('foods') && has('foods')) {
    const items = _joinAry(recs.foods, (f) => {
      if (!f?.name) return null
      const n = f.nature ? `性味${f.nature}` : ''
      const e = f.effect ? `功效：${f.effect}` : ''
      return [f.name, n, e].filter(Boolean).join('｜')
    }, 4)
    if (items) lines.push(`- 药膳食疗推荐：${items}。`)
  }
  if (intents.has('acupoints') && has('acupoints')) {
    const items = _joinAry(recs.acupoints, (a) => {
      if (!a?.name) return null
      const l = a.location ? `取穴${a.location}` : ''
      const m = a.method ? `方法${a.method}` : ''
      return [a.name, l, m].filter(Boolean).join('｜')
    }, 4)
    if (items) lines.push(`- 经络穴位调理：${items}。`)
  }
  if (intents.has('exercises') && has('exercises')) {
    const items = _joinAry(recs.exercises, (e) => {
      if (!e?.name) return null
      const ef = e.effect ? `功效${e.effect}` : ''
      const m = e.method ? `方法${e.method}` : ''
      return [e.name, ef, m].filter(Boolean).join('｜')
    }, 4)
    if (items) lines.push(`- 运动方案推荐：${items}。`)
  }
  if (intents.has('therapy_process') && has('therapy_process')) {
    const items = _joinAry(recs.therapy_process, (t) => {
      if (!t?.name) return null
      const b = t.base ? `基础${t.base}` : ''
      const s = t.sequence ? `顺序${t.sequence}` : ''
      const f = t.frequency ? `频率${t.frequency}` : ''
      return [t.name, b, s, f].filter(Boolean).join('｜')
    }, 3)
    if (items) lines.push(`- 专属疗法过程：${items}。`)
  }
  if (intents.has('health_knowledge') && has('health_knowledge')) {
    const items = _joinAry(recs.health_knowledge, (h) => {
      if (!h?.category && !h?.content) return null
      const c = h.content ? h.content : ''
      return h.category ? `【${h.category}】${c}` : c
    }, 3)
    if (items) lines.push(`- 养生知识：${items}。`)
  }
  if (intents.has('precautions') && has('precautions')) {
    const items = recs.precautions.slice(0, 6).join('；')
    if (items) lines.push(`- 温馨注意事项：${items}。`)
  }

  // 兼夹体质（得分≥40）：补充 2 个食疗 + 2 个穴位
  if (constitutionRecs && typeof constitutionRecs === 'object') {
    const biasedKeys = Object.keys(constitutionRecs)
      .filter((k) => k !== primaryKey && (scores[k] ?? 0) >= 40)
      .slice(0, 2)
    for (const k of biasedKeys) {
      const cname = constitutionNames[k] || k
      const cr = constitutionRecs[k] || {}
      const parts = []
      if (intents.has('foods') && Array.isArray(cr.foods) && cr.foods.length) {
        const foods = cr.foods.slice(0, 2).map((f) => f.name).filter(Boolean).join('、')
        if (foods) parts.push(`食疗${foods}`)
      }
      if (intents.has('acupoints') && Array.isArray(cr.acupoints) && cr.acupoints.length) {
        const acu = cr.acupoints.slice(0, 2).map((a) => a.name).filter(Boolean).join('、')
        if (acu) parts.push(`穴位${acu}`)
      }
      if (intents.has('exercises') && Array.isArray(cr.exercises) && cr.exercises.length) {
        const ex = cr.exercises.slice(0, 2).map((e) => e.name).filter(Boolean).join('、')
        if (ex) parts.push(`运动${ex}`)
      }
      if (parts.length) {
        lines.push(`【兼夹体质「${cname}」补充】${parts.join('；')}。`)
      }
    }
    // 若用户只问得分<40 倾向体质（secondary）且命中，也加 1 条食疗
    for (const sk of secKeys) {
      if (biasedKeys.includes(sk)) continue
      const cr = constitutionRecs[sk]
      if (!cr) continue
      const cname = constitutionNames[sk] || sk
      const parts = []
      if (intents.has('foods') && Array.isArray(cr.foods) && cr.foods.length) {
        parts.push(`食疗${cr.foods[0].name}`)
      }
      if (intents.has('acupoints') && Array.isArray(cr.acupoints) && cr.acupoints.length) {
        parts.push(`穴位${cr.acupoints[0].name}`)
      }
      if (parts.length) {
        lines.push(`【兼夹倾向「${cname}」补充】${parts.join('；')}。`)
      }
    }
  }

  lines.push('用户原问题：')
  let joined = lines.join('\n')
  // 保险：控制前缀长度 ≤ 750 字，给用户原问题留 250 字
  if (joined.length > 750) joined = joined.slice(0, 750) + '\n...（系统：前缀已截断，如需要更多推荐条目请在追问中指明具体体质或推荐项。）\n用户原问题：'
  return joined
}

/**
 * 在 store.sendMessage 发送之前，把 ground truth 前缀拼到 text 前。
 * 返回新的（或原）文本字符串。
 */
function _augmentTextWithPlan(text) {
  try {
    const t = typeof text === 'string' ? text : ''
    const loaded = Boolean(recommendations.value || Object.keys(constitutionRecommendations.value || {}).length)
    if (!loaded) return t
    // 若没 seed，但 user 直接在 Result 页追问（极少见）：也允许附加（反正推荐已加载）
    const intents = _detectIntents(t)
    if (intents.has('__chatter__')) return t
    // 如果意图没匹配，但是我们在 seed 模式下且文本是中文问题（≥3字），也带完整方案做兜底（一般是模糊问题 like "帮我说说" / "讲清楚" / "给建议"）
    if (intents.size === 0) {
      const isLikelyQuestion = /[吗呢怎么什么为什么为何给说说讲讲建议方案调理推荐注意]/.test(t) && t.length >= 3
      if (!isLikelyQuestion) return t
      // 默认带上全部 6 类
      for (const k of Object.keys(_INTENT_PATTERNS)) intents.add(k)
    }
    const prefix = _buildPlanPrefix(intents, {
      recommendations: recommendations.value,
      constitutionRecs: constitutionRecommendations.value,
      result: result.value,
    })
    if (!prefix) return t
    return prefix + t
  } catch (e) {
    console.warn('[Result] 调理方案前缀注入失败，使用原文：', e)
    return typeof text === 'string' ? text : ''
  }
}

// 包装 store.sendMessage：拦截自由文本 + 6 个 askXxx 按钮（askQuick→sendMessage）
let _storePatched = false
let _originalSendMessage = null
function _installStoreSendWrapper() {
  if (_storePatched) return
  _originalSendMessage = agentChat.sendMessage.bind(agentChat)
  agentChat.sendMessage = async (text, opts) => {
    const augmented = _augmentTextWithPlan(text)
    return _originalSendMessage(augmented, opts)
  }
  _storePatched = true
}
function _uninstallStoreSendWrapper() {
  if (!_storePatched || !_originalSendMessage) return
  agentChat.sendMessage = _originalSendMessage
  _originalSendMessage = null
  _storePatched = false
}

onUnmounted(() => {
  _uninstallStoreSendWrapper()
})

// 问 AI 的各类预设追问
const safeAsk = async (text) => {
  if (!isLoggedIn.value) {
    seed401Hint.value = true
    onPanelError('请先登录后再追问（右上角或"立即登录"按钮）。', 401)
    return
  }
  if (!panelRef.value || typeof panelRef.value.askQuick !== 'function') {
    onPanelError('聊天面板尚未就绪，请稍后再试。', 'panel_not_ready')
    return
  }
  try {
    await panelRef.value.askQuick(text)
  } catch (err) {
    onPanelError(
      (err && err.userMessage) || (err && err.message) || '发送追问失败，请稍后再试。',
      (err && err.status) || (err && err.code) || 'ask_error'
    )
  }
}

const askAcupoint = (a) => {
  if (!a || !a.name) return
  const pn = (agentChat.seed_source && agentChat.seed_source.primary_name) || primaryName.value
  safeAsk(
    `为什么推荐${a.name}？我这种${pn}适合每天按几分钟？有什么操作禁忌吗？取穴不准会怎样？`
  )
}
const askFood = (f) => {
  if (!f || !f.name) return
  const pn = (agentChat.seed_source && agentChat.seed_source.primary_name) || primaryName.value
  const nature = f.nature || '未标注'
  safeAsk(
    `推荐的${f.name}，性味${nature}，我这种${pn}搭配什么一起吃更好？一周吃几次？有没有配伍禁忌（和我可能吃的药冲突）？`
  )
}
const askExercise = (e) => {
  if (!e || !e.name) return
  const pn = (agentChat.seed_source && agentChat.seed_source.primary_name) || primaryName.value
  const method = e.method || '10-15 分钟'
  safeAsk(
    `${e.name} 这种运动，${pn}在一天里什么时段做最合适？每次${method}就够吗？做的时候要注意什么呼吸配合吗？`
  )
}
const askTherapy = (tp) => {
  if (!tp || !tp.name) return
  const pn = (agentChat.seed_source && agentChat.seed_source.primary_name) || primaryName.value
  const secNames = secondaryNamesForPrompt.value
  const base = tp.base || '未说明'
  const sequence = tp.sequence || '未说明'
  const frequency = tp.frequency || '依情况'
  safeAsk(
    `${tp.name}疗法（基础：${base}；顺序：${sequence}），适合我这种${pn}${secNames ? '兼夹' + secNames : ''}多久做一次？频率${frequency}下，单次多久？在家能自己操作吗？还是要去养生馆/医院？`
  )
}
const askHealthKnowledge = (hk) => {
  if (!hk || !hk.category) return
  const pn = (agentChat.seed_source && agentChat.seed_source.primary_name) || primaryName.value
  safeAsk(
    `关于「${hk.category}」这条健康科普，能结合我${pn}的实际情况再展开讲一讲吗？如果有具体例子或误区提醒就更好了`
  )
}
const askPrecaution = (item) => {
  if (!item) return
  const pn = (agentChat.seed_source && agentChat.seed_source.primary_name) || primaryName.value
  safeAsk(
    `注意事项里提到「${item}」——能详细说说为什么${pn}要特别注意这一点吗？不遵守的话常见后果是什么？如果不小心违反了，有什么补救建议？`
  )
}
const askReasonBreakdown = () => {
  if (!agentChat.seed_source) return
  const pn = agentChat.seed_source.primary_name || primaryName.value
  safeAsk(
    `这份问卷我为什么被判定为${pn}？能把每项体质得分和判定规则拆解给我看吗？`
  )
}

const initRadarChart = () => {
  if (!radarChart.value) return
  const chart = echarts.init(radarChart.value)
  const option = {
    title: {
      text: '体质偏颇分析',
      left: 'center',
      textStyle: { color: '#5c4a3d', fontFamily: 'Noto Serif SC', fontSize: 18 },
    },
    radar: {
      indicator: Object.keys(constitutionNames).map((k) => ({ name: constitutionNames[k], max: 100 })),
      radius: '60%',
      center: ['50%', '55%'],
      splitArea: {
        areaStyle: { color: ['#fdfbf7', '#f5f0e6', '#e8dcc4', '#c0b298'].reverse() },
      },
      axisLine: { lineStyle: { color: '#8b7355' } },
    },
    series: [
      {
        type: 'radar',
        data: [
          {
            value: Object.keys(constitutionNames).map((k) => result.value?.scores[k] || 0),
            areaStyle: { color: 'rgba(139, 115, 85, 0.4)' },
            lineStyle: { color: '#8b7355', width: 2 },
          },
        ],
      },
    ],
  }
  chart.setOption(option)
}
</script>
