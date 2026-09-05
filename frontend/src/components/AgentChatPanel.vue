<template>
  <div
    :class="[
      'flex flex-col bg-paper border border-border rounded-sm shadow-lg overflow-hidden',
      mode === 'page' ? 'h-[calc(100vh-150px)] min-h-[480px]' : 'h-full min-h-[400px]',
    ]"
  >
    <!-- 1. 顶部标题栏（page 模式才显示） -->
    <template v-if="mode === 'page'">
      <div class="bg-primary text-paper px-5 py-3 border-b-2 border-secondary flex items-center justify-between flex-shrink-0">
        <div class="flex items-center space-x-3">
          <Bot class="w-7 h-7 flex-shrink-0" />
          <div>
            <h2 class="text-lg md:text-xl font-serif font-bold tracking-widest">中医多智能体问诊</h2>
            <p class="text-xs text-paper/80 font-serif">三级协同 Agent · 症状分析 / 体质推理 / 方案生成</p>
          </div>
        </div>
        <div class="flex items-center space-x-2 flex-shrink-0">
          <span v-if="restoring" class="hidden sm:inline-flex items-center text-xs text-paper/80 font-serif italic">
            <Loader2 class="w-3 h-3 mr-1 animate-spin" /> 恢复中
          </span>
          <span class="hidden sm:inline text-xs text-paper/70 font-serif">工具模式</span>
          <span
            :class="[
              'px-3 py-1 rounded-full text-xs font-serif border flex items-center',
              toolsMode === 'mcp'
                ? 'bg-green-100 text-green-800 border-green-300'
                : toolsMode === 'local'
                  ? 'bg-amber-100 text-amber-800 border-amber-300'
                  : 'bg-gray-100 text-gray-600 border-gray-300',
            ]"
          >
            <component :is="toolsMode === 'mcp' ? Cable : Cpu" class="w-3 h-3 mr-1" />
            {{ toolsMode === 'mcp' ? 'MCP 协议' : toolsMode === 'local' ? '本地调用' : '加载中' }}
          </span>
        </div>
      </div>

      <!-- 会话恢复/过期提示条（page 模式横幅） -->
      <div
        v-if="restoreHint"
        class="flex-shrink-0 px-4 py-2 text-xs font-serif bg-amber-50 border-b border-amber-200 text-amber-900 flex items-center"
      >
        <AlertTriangle class="w-3.5 h-3.5 mr-2 text-amber-600 flex-shrink-0" />
        <span>{{ restoreHint }}</span>
      </div>
    </template>

    <!-- mini 模式：右上角小 toast（恢复提示） -->
    <div
      v-if="mode === 'mini' && miniToast"
      class="flex-shrink-0 self-end mr-3 -mt-1 mb-1 z-10 rounded px-3 py-1 text-xs text-paper font-serif bg-primary/90 shadow"
    >
      {{ miniToast }}
    </div>

    <!-- 2. 状态条 -->
    <div
      :class="[
        'bg-white border-b border-border px-4 py-2 flex flex-wrap items-center gap-x-4 gap-y-2 flex-shrink-0',
        compact ? 'text-xs' : 'text-sm',
      ]"
    >
      <template v-if="mode !== 'mini'">
        <div class="flex items-center text-secondary font-serif">
          <Hash :class="compact ? 'w-3.5 h-3.5' : 'w-4 h-4'" class="mr-1 text-primary" />
          轮次 <span class="font-bold text-primary ml-1">{{ currentTurn }}</span>
        </div>

        <div class="flex items-center text-secondary font-serif">
          <Stethoscope :class="compact ? 'w-3.5 h-3.5' : 'w-4 h-4'" class="mr-1 text-primary" />
          <span class="mr-1">症状</span>
          <div v-if="accumulatedSymptoms.length" class="flex flex-wrap gap-1">
            <span
              v-for="s in accumulatedSymptoms"
              :key="s"
              :class="[compact ? 'px-1.5 py-0.5 text-[11px]' : 'px-2 py-0.5 text-xs', 'bg-[#f5f0e6] border border-border rounded-full text-primary']"
            >{{ s }}</span>
          </div>
          <span v-else class="text-xs text-[#c0b298]">尚未采集</span>
        </div>

        <div class="flex items-center text-secondary font-serif">
          <Zap :class="compact ? 'w-3.5 h-3.5' : 'w-4 h-4'" class="mr-1 text-primary" />
          <span class="mr-1">置信度</span>
          <div :class="compact ? 'w-16' : 'w-24'" class="h-2 bg-gray-200 rounded-full overflow-hidden">
            <div
              :class="['h-full rounded-full transition-all duration-500', confidenceColor]"
              :style="{ width: currentConfidence * 100 + '%' }"
            ></div>
          </div>
          <span
            :class="[
              'ml-1 font-bold',
              compact ? 'text-[11px]' : 'text-xs',
              currentConfidence < 0.6 && currentConfidence > 0 ? 'text-red-600' : 'text-primary',
            ]"
          >
            {{ currentConfidence > 0 ? (currentConfidence * 100).toFixed(0) + '%' : '--' }}
          </span>
          <AlertTriangle
            v-if="currentConfidence > 0 && currentConfidence < 0.6"
            :class="compact ? 'w-3 h-3' : 'w-3.5 h-3.5'"
            class="ml-1 text-red-600"
          />
        </div>

        <div class="flex items-center text-secondary font-serif">
          <Clock :class="compact ? 'w-3.5 h-3.5' : 'w-4 h-4'" class="mr-1 text-primary" />
          <span class="mr-1">延迟</span>
          <span :class="['font-bold', latencyOk === null ? 'text-[#c0b298]' : latencyOk ? 'text-green-600' : 'text-red-600']">
            {{ latencyLabel }}
          </span>
          <span class="text-xs text-[#c0b298]">/ 目标 {{ latencyTarget }}s</span>
        </div>
      </template>

      <!-- mini 模式：只展示体质 + 轮次；其它藏进 tooltip -->
      <template v-else>
        <div class="flex items-center text-secondary font-serif">
          <div v-if="seedSource" class="flex items-center mr-3">
            <span class="text-[#c0b298] mr-1">体质</span>
            <span class="font-bold text-primary">{{ seedSource.primary_name }}</span>
            <span v-if="seedSource.secondary_names && seedSource.secondary_names.length" class="text-secondary ml-1">
              兼 {{ seedSource.secondary_names.join('、') }}
            </span>
          </div>
          <Hash class="w-3.5 h-3.5 mr-1 text-primary" />
          轮次 <span class="font-bold text-primary ml-1">{{ currentTurn }}</span>

          <div class="relative ml-2">
            <Info class="w-3.5 h-3.5 text-[#c0b298] hover:text-primary cursor-help" @mouseenter="showMiniTip = true" @mouseleave="showMiniTip = false" />
            <div
              v-if="showMiniTip"
              class="absolute right-0 top-5 w-64 bg-white border border-border rounded shadow-md p-2 text-[11px] text-secondary z-20 space-y-1"
            >
              <p><span class="text-primary font-semibold">症状：</span>{{ accumulatedSymptoms.length ? accumulatedSymptoms.join('、') : '尚未采集' }}</p>
              <p>
                <span class="text-primary font-semibold">置信度：</span>
                <span :class="confidenceColorText">
                  {{ currentConfidence > 0 ? (currentConfidence * 100).toFixed(0) + '%' : '--' }}
                </span>
              </p>
              <p>
                <span class="text-primary font-semibold">延迟：</span>
                <span :class="latencyOk === null ? 'text-[#c0b298]' : latencyOk ? 'text-green-600' : 'text-red-600'">{{ latencyLabel }}</span>
                <span class="text-[#c0b298]"> / 目标 {{ latencyTarget }}s</span>
              </p>
            </div>
          </div>
        </div>
      </template>
    </div>

    <!-- 3. 对话气泡区 -->
    <div ref="scrollArea" class="flex-1 overflow-y-auto px-4 py-4 space-y-4 bg-paper">
      <div
        v-if="!messages.length"
        class="h-full flex flex-col items-center justify-center text-center text-[#c0b298] font-serif"
      >
        <Bot :class="compact ? 'w-12 h-12' : 'w-16 h-16'" class="mb-4 text-primary/30" />
        <p :class="compact ? 'text-base' : 'text-lg'">欢迎使用中医多智能体问诊</p>
        <p :class="compact ? 'text-xs mt-1' : 'text-sm mt-2'">
          请描述您的症状、舌象、脉象，<br />三级 Agent 将协同为您辨证并生成调理方案。
        </p>
      </div>

      <div
        v-for="(msg, idx) in messages"
        :key="idx"
        :class="['flex', msg.role === 'user' ? 'justify-end' : 'justify-start']"
      >
        <!-- 用户消息 -->
        <div
          v-if="msg.role === 'user'"
          :class="[
            'max-w-[75%] bg-primary text-paper rounded-lg rounded-tr-none px-4 py-2.5 shadow-sm',
            compact ? 'text-xs' : 'text-sm',
          ]"
        >
          <p class="whitespace-pre-wrap break-words font-serif">{{ msg.content }}</p>
        </div>

        <!-- 助手消息 -->
        <div v-else class="w-full max-w-3xl">
          <div
            :class="[
              'bg-white border border-border rounded-lg rounded-tl-none px-4 py-3 shadow-sm space-y-3',
              compact ? 'text-xs' : 'text-sm',
            ]"
          >
            <!-- 错误 -->
            <div
              v-if="msg.error"
              class="flex items-start text-red-700 bg-red-50 border border-red-200 rounded p-3"
            >
              <AlertCircle :class="compact ? 'w-3.5 h-3.5' : 'w-4 h-4'" class="mr-2 mt-0.5 flex-shrink-0" />
              <p>{{ msg.content }}</p>
            </div>

            <!-- seeded 阶段：问卷锚定 -->
            <template v-else-if="msg.response && msg.response.stage === 'seeded'">
              <div
                class="flex items-center text-secondary font-serif font-bold border-b border-border pb-1.5"
              >
                <CheckCircle2 class="w-4 h-4 mr-1.5 text-green-600" />
                <span>已锚定问卷测评结果</span>
              </div>
              <div class="bg-green-50 border border-green-200 rounded p-3 space-y-2">
                <div class="flex flex-wrap gap-3 items-center text-[#2d5016]">
                  <span class="inline-flex items-center bg-green-100 border border-green-300 rounded-full px-2.5 py-0.5 font-bold">
                    ✅ #{{ msg.response.seed_source?.assessment_id || 'N' }}
                  </span>
                  <span>
                    主 <span class="font-bold">{{ msg.response.seed_source?.primary_name || '主体质' }}</span>
                    <template v-if="msg.response.seed_source?.secondary_names?.length">
                      ；兼夹 <span class="font-bold">{{ msg.response.seed_source.secondary_names.join('、') }}</span>
                    </template>
                  </span>
                </div>
                <div v-if="msg.response.seed_source?.reason" class="text-xs text-[#2d5016] bg-white/60 border border-green-200 rounded p-2">
                  <p class="font-semibold mb-0.5 flex items-center"><BookOpenCheck class="w-3.5 h-3.5 mr-1" />判定依据</p>
                  <div class="md-content" v-html="renderMd(msg.response.seed_source.reason)"></div>
                </div>
                <div v-if="msg.response.seed_source?.scores" class="text-[11px] text-[#4b6b3a]">
                  <span class="font-semibold">各项得分：</span>
                  {{ Object.entries(msg.response.seed_source.scores).map(([k, v]) => `${k}:${v}`).join('  ') }}
                </div>
              </div>
            </template>

            <!-- clarify 阶段 -->
            <template v-else-if="msg.response && msg.response.stage === 'clarify'">
              <div class="flex items-center text-secondary font-serif font-bold border-b border-border pb-1.5">
                <HelpCircle class="w-4 h-4 mr-1.5 text-amber-600" />
                <span>需要更多信息以明确辨证</span>
                <span v-if="msg.response.rejected" class="ml-2 text-xs px-2 py-0.5 bg-red-100 text-red-700 rounded-full">
                  置信度不足，暂缓判定
                </span>
              </div>
              <div
                v-if="msg.response.clarification"
                class="bg-amber-50 border-l-4 border-amber-400 p-3 rounded-r text-amber-900 space-y-1"
              >
                <p class="font-semibold flex items-center">
                  <HelpCircle class="w-4 h-4 mr-1.5" />澄清问题
                </p>
                <div class="pl-1" v-html="renderMd(msg.response.clarification)"></div>
              </div>
              <div v-if="msg.response.symptom_result" class="text-xs text-[#6b5c51] bg-paper border border-border rounded p-2">
                <span class="font-semibold text-primary">当前采集：</span>
                {{ formatSymptomSummary(msg.response.symptom_result) }}
              </div>
            </template>

            <!-- plan 阶段 -->
            <template v-else-if="msg.response && msg.response.stage === 'plan'">
              <!-- 症状分析结果 -->
              <div v-if="msg.response.symptom_result" class="border border-border rounded p-3 bg-paper">
                <h4
                  :class="[
                    'font-serif font-bold text-secondary mb-2 flex items-center border-b border-border pb-1',
                    compact ? 'text-xs' : 'text-sm',
                  ]"
                >
                  <Stethoscope class="w-4 h-4 mr-1.5 text-primary" />症状分析结果
                </h4>
                <div class="text-xs text-[#6b5c51] space-y-1">
                  <p>
                    <span class="font-semibold text-primary">症状：</span>{{ formatSymptomSummary(msg.response.symptom_result) }}
                  </p>
                  <p v-if="msg.response.symptom_result.completeness !== undefined">
                    <span class="font-semibold text-primary">信息完整度：</span>{{ msg.response.symptom_result.completeness }}
                  </p>
                </div>
              </div>

              <!-- 体质推理结果 -->
              <div v-if="msg.response.constitution_result" class="border-2 border-primary/40 rounded p-3 bg-white">
                <h4
                  :class="[
                    'font-serif font-bold text-secondary mb-2 flex items-center border-b border-border pb-1',
                    compact ? 'text-xs' : 'text-sm',
                  ]"
                >
                  <Brain class="w-4 h-4 mr-1.5 text-primary" />体质推理结果
                </h4>
                <div :class="['grid gap-2 mb-2 text-xs', compact ? 'grid-cols-2' : 'grid-cols-2 md:grid-cols-4']">
                  <div class="bg-paper rounded px-2 py-1 border border-border">
                    <p class="text-[#c0b298]">主体质</p>
                    <p class="font-serif font-bold text-primary text-sm">{{ msg.response.constitution_result.constitution_name || '未定' }}</p>
                  </div>
                  <div v-if="msg.response.constitution_result.secondary" class="bg-paper rounded px-2 py-1 border border-border">
                    <p class="text-[#c0b298]">兼夹</p>
                    <p class="font-serif font-bold text-secondary text-sm">
                      {{ formatSecondary(msg.response.constitution_result.secondary) }}
                    </p>
                  </div>
                  <div v-if="msg.response.constitution_result.syndrome" class="bg-paper rounded px-2 py-1 border border-border">
                    <p class="text-[#c0b298]">证型</p>
                    <p class="font-serif font-bold text-secondary text-sm">{{ msg.response.constitution_result.syndrome }}</p>
                  </div>
                  <div class="bg-paper rounded px-2 py-1 border border-border">
                    <p class="text-[#c0b298]">置信度</p>
                    <p :class="['font-serif font-bold text-sm', confidenceClass(msg.response.constitution_result.confidence)]">
                      {{ (msg.response.constitution_result.confidence * 100).toFixed(0) }}%
                    </p>
                  </div>
                </div>
                <div
                  v-if="msg.response.constitution_result.reasoning"
                  class="text-xs text-[#6b5c51] bg-paper border border-border rounded p-2"
                >
                  <p class="font-semibold text-primary mb-1">推理依据</p>
                  <div class="md-content" v-html="renderMd(msg.response.constitution_result.reasoning)"></div>
                </div>
              </div>

              <!-- 方案卡片 -->
              <div
                v-if="msg.response.plan_result && msg.response.plan_result.plan"
                class="border border-border rounded p-3 bg-paper"
              >
                <h4
                  :class="[
                    'font-serif font-bold text-secondary mb-3 flex items-center border-b border-border pb-1',
                    compact ? 'text-xs' : 'text-sm',
                  ]"
                >
                  <ClipboardList class="w-4 h-4 mr-1.5 text-primary" />调理方案
                </h4>
                <div class="grid md:grid-cols-3 gap-3">
                  <!-- 穴位 -->
                  <div>
                    <h5 :class="compact ? 'text-xs' : 'text-sm'" class="font-serif font-semibold text-secondary mb-2 flex items-center">
                      <Wind class="w-4 h-4 mr-1 text-[#b8860b]" />穴位推荐
                    </h5>
                    <div class="space-y-2">
                      <div
                        v-for="(a, i) in msg.response.plan_result.plan.acupoints"
                        :key="'a' + i"
                        class="bg-white rounded p-2 border-l-2 border-[#b8860b] shadow-sm"
                      >
                        <p class="font-serif font-bold text-secondary text-sm">{{ a.name }}</p>
                        <p v-if="a.location" class="text-xs text-[#6b5c51]">取穴：{{ a.location }}</p>
                        <p v-if="a.method" class="text-xs text-[#6b5c51]">方法：{{ a.method }}</p>
                        <p v-if="a.reason" class="text-xs text-amber-700 bg-amber-50 rounded px-1.5 py-1 mt-1">
                          ✨ {{ a.reason }}
                        </p>
                      </div>
                      <p v-if="!msg.response.plan_result.plan.acupoints?.length" class="text-xs text-[#c0b298] italic">
                        暂无
                      </p>
                    </div>
                  </div>
                  <!-- 食材 -->
                  <div>
                    <h5 :class="compact ? 'text-xs' : 'text-sm'" class="font-serif font-semibold text-secondary mb-2 flex items-center">
                      <Apple class="w-4 h-4 mr-1 text-[#556b2f]" />食疗推荐
                    </h5>
                    <div class="space-y-2">
                      <div
                        v-for="(f, i) in msg.response.plan_result.plan.foods"
                        :key="'f' + i"
                        class="bg-white rounded p-2 border-l-2 border-[#556b2f] shadow-sm"
                      >
                        <p class="font-serif font-bold text-secondary text-sm">{{ f.name }}</p>
                        <p v-if="f.nature" class="text-xs text-[#6b5c51]">性味：{{ f.nature }}</p>
                        <p v-if="f.effect" class="text-xs text-[#6b5c51]">功效：{{ f.effect }}</p>
                        <p v-if="f.reason" class="text-xs text-amber-700 bg-amber-50 rounded px-1.5 py-1 mt-1">
                          ✨ {{ f.reason }}
                        </p>
                      </div>
                      <p v-if="!msg.response.plan_result.plan.foods?.length" class="text-xs text-[#c0b298] italic">
                        暂无
                      </p>
                    </div>
                  </div>
                  <!-- 运动 -->
                  <div>
                    <h5 :class="compact ? 'text-xs' : 'text-sm'" class="font-serif font-semibold text-secondary mb-2 flex items-center">
                      <Activity class="w-4 h-4 mr-1 text-[#4682b4]" />运动推荐
                    </h5>
                    <div class="space-y-2">
                      <div
                        v-for="(e, i) in msg.response.plan_result.plan.exercises"
                        :key="'e' + i"
                        class="bg-white rounded p-2 border-l-2 border-[#4682b4] shadow-sm"
                      >
                        <p class="font-serif font-bold text-secondary text-sm">{{ e.name }}</p>
                        <p v-if="e.effect" class="text-xs text-[#6b5c51]">功效：{{ e.effect }}</p>
                        <p v-if="e.method" class="text-xs text-[#6b5c51]">方法：{{ e.method }}</p>
                        <p v-if="e.reason" class="text-xs text-amber-700 bg-amber-50 rounded px-1.5 py-1 mt-1">
                          ✨ {{ e.reason }}
                        </p>
                      </div>
                      <p v-if="!msg.response.plan_result.plan.exercises?.length" class="text-xs text-[#c0b298] italic">
                        暂无
                      </p>
                    </div>
                  </div>
                </div>
              </div>

              <!-- 注意事项 -->
              <div
                v-if="
                  msg.response.plan_result &&
                  msg.response.plan_result.plan &&
                  msg.response.plan_result.plan.precautions?.length
                "
                class="p-3 bg-amber-50 border border-amber-200 rounded"
              >
                <h5 :class="compact ? 'text-xs' : 'text-sm'" class="font-serif font-bold text-amber-800 mb-1.5 flex items-center">
                  <span class="w-1 h-4 bg-amber-500 mr-2"></span>注意事项
                </h5>
                <ul class="list-disc list-inside space-y-0.5 text-xs text-amber-800">
                  <li v-for="(item, i) in msg.response.plan_result.plan.precautions" :key="i">{{ item }}</li>
                </ul>
              </div>
            </template>

            <!-- 普通/兜底 -->
            <p v-else class="text-[#6b5c51] font-serif">{{ msg.content }}</p>

            <!-- Agent 调用链路（可折叠） -->
            <div
              v-if="msg.response && msg.response.trace && msg.response.trace.length"
              class="border-t border-border pt-2 mt-1"
            >
              <button
                @click="msg.traceExpanded = !msg.traceExpanded"
                class="flex items-center text-xs text-[#8b7355] hover:text-secondary font-serif"
              >
                <component :is="msg.traceExpanded ? ChevronDown : ChevronRight" class="w-3.5 h-3.5 mr-1" />
                Agent 调用链路（{{ msg.response.trace.length }} 步）
              </button>
              <div v-if="msg.traceExpanded" class="mt-2 space-y-1">
                <div
                  v-for="(t, i) in msg.response.trace"
                  :key="i"
                  class="flex flex-wrap items-center gap-x-2 gap-y-0.5 text-xs bg-paper border border-border rounded px-2 py-1"
                >
                  <span class="font-serif font-bold text-secondary">{{ t.agent || '未知' }}</span>
                  <span v-if="t.degraded === true" class="px-1.5 py-0.5 bg-red-100 text-red-700 rounded">已降级</span>
                  <span v-else-if="t.degraded === false" class="px-1.5 py-0.5 bg-green-100 text-green-700 rounded">
                    正常
                  </span>
                  <span v-if="t.tool" class="px-1.5 py-0.5 bg-[#f5f0e6] text-primary rounded flex items-center">
                    <Wrench class="w-3 h-3 mr-0.5" />{{ t.tool }}
                    <component
                      :is="t.tool_ok ? CheckCircle2 : XCircle"
                      :class="['w-3 h-3 ml-1', t.tool_ok ? 'text-green-600' : 'text-red-600']"
                    />
                  </span>
                  <span v-if="t.event === 'accept'" class="px-1.5 py-0.5 bg-green-100 text-green-700 rounded">采纳</span>
                  <span v-if="t.event === 'reject'" class="px-1.5 py-0.5 bg-red-100 text-red-700 rounded">拒答</span>
                  <span v-if="t.elapsed !== undefined" class="text-[#6b5c51] flex items-center">
                    <Clock class="w-3 h-3 mr-0.5" />{{ t.elapsed }}s
                  </span>
                  <span v-if="t.confidence !== undefined" class="text-[#6b5c51]">
                    置信度 {{ (t.confidence * 100).toFixed(0) }}%
                  </span>
                  <span v-if="t.note" class="text-amber-700 italic">{{ t.note }}</span>
                  <span v-if="t.reason" class="text-red-600 italic">{{ t.reason }}</span>
                  <span v-if="t.error" class="text-red-600 italic">错误：{{ t.error }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 加载占位 -->
      <div v-if="store.loading" class="flex justify-start">
        <div
          class="bg-white border border-border rounded-lg rounded-tl-none px-4 py-3 shadow-sm flex items-center text-[#8b7355] font-serif"
          :class="compact ? 'text-xs' : 'text-sm'"
        >
          <Loader2 class="w-4 h-4 mr-2 animate-spin" />
          三级 Agent 协同推理中...
        </div>
      </div>
    </div>

    <!-- 4. 底部输入栏 -->
    <div class="bg-white border-t-2 border-border px-3 py-2.5 flex items-end gap-2 flex-shrink-0">
      <textarea
        ref="inputArea"
        v-model="userInput"
        @keydown.enter.exact.prevent="send"
        @input="autoResize"
        :rows="compact ? 2 : 1"
        :disabled="store.loading"
        placeholder="描述您的症状、舌象、脉象... 回车发送"
        :class="[
          'flex-1 resize-none border border-border rounded-lg px-3 py-2 font-serif text-ink bg-paper focus:outline-none focus:ring-2 focus:ring-primary/40 focus:border-primary disabled:opacity-50 max-h-32',
          compact ? 'text-xs' : 'text-sm',
        ]"
        :style="{ minHeight: compact ? '56px' : '40px' }"
      ></textarea>
      <button
        @click="send"
        :disabled="store.loading || !userInput.trim()"
        :class="[
          'flex items-center bg-primary text-paper rounded-lg hover:bg-secondary transition-colors disabled:opacity-40 disabled:cursor-not-allowed font-serif flex-shrink-0',
          compact ? 'px-3 py-1.5 text-xs' : 'px-4 py-2 text-sm',
        ]"
      >
        <Send :class="compact ? 'w-3.5 h-3.5 mr-1' : 'w-4 h-4 mr-1'" />
        发送
      </button>
      <button
        @click="reset"
        :disabled="store.loading || !sessionId"
        :class="[
          'flex items-center bg-white text-secondary border border-border rounded-lg hover:bg-paper transition-colors disabled:opacity-40 disabled:cursor-not-allowed font-serif flex-shrink-0',
          compact ? 'px-2.5 py-1.5' : 'px-3 py-2',
          compact ? 'text-xs' : 'text-sm',
        ]"
        title="重置会话"
      >
        <RotateCcw :class="compact ? 'w-3.5 h-3.5' : 'w-4 h-4'" />
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick, onMounted, computed, watch } from 'vue'
import axios from '@/api'
import { marked } from 'marked'
import { useAgentChatStore } from '@/store/agentChat'
import {
  Bot,
  Cable,
  Cpu,
  Hash,
  Stethoscope,
  Zap,
  Clock,
  AlertTriangle,
  HelpCircle,
  Brain,
  ClipboardList,
  Wind,
  Apple,
  Activity,
  ChevronDown,
  ChevronRight,
  Loader2,
  Send,
  RotateCcw,
  AlertCircle,
  Wrench,
  CheckCircle2,
  XCircle,
  Info,
  BookOpenCheck,
} from 'lucide-vue-next'

marked.setOptions({ breaks: true, gfm: true })

const props = defineProps({
  mode: { type: String, default: 'page' }, // 'page' | 'mini'
  compact: { type: Boolean, default: false },
  skipRestore: { type: Boolean, default: false },
})

const emit = defineEmits(['seeded', 'error', 'session-changed'])

// mini 自动强制 compact
const compact = computed(() => props.compact || props.mode === 'mini')

const store = useAgentChatStore()

const userInput = ref('')
const scrollArea = ref(null)
const inputArea = ref(null)
const toolsMode = ref('') // '' | 'mcp' | 'local'
const restoring = ref(false)
const restoreHint = ref('')
const miniToast = ref('')
const showMiniTip = ref(false)

// 响应式从 store 取；computed 带 setter 兼容直接修改（不常用，仅 v-for 场景）
const messages = computed({
  get: () => store.messages,
  set: () => {},
})
const sessionId = computed(() => store.sessionId)
const seedSource = computed(() => store.seed_source)

// 向外透出：父组件 Result.vue 通过 ref 调用
function askQuick(text) {
  return store.askQuick(text)
}
defineExpose({ askQuick })

// 新消息到就滚到底
watch(
  () => store.messages.length,
  () => {
    scrollToBottom()
  }
)

// sessionId 变化对外通知
watch(
  () => store.sessionId,
  (v) => emit('session-changed', v)
)

// seeded 对外广播（仅当 seed_source 从无到有时）
watch(
  () => store.seed_source,
  (v) => {
    if (v) emit('seeded', v)
  },
  { immediate: false }
)

// ---------------- 状态条数据（取最近一条助手响应） ----------------
const currentTurn = computed(() => {
  for (let i = messages.value.length - 1; i >= 0; i--) {
    const r = messages.value[i].response
    if (r && r.turn !== undefined) return r.turn
  }
  return 0
})
const accumulatedSymptoms = computed(() => {
  for (let i = messages.value.length - 1; i >= 0; i--) {
    const r = messages.value[i].response
    if (r && r.symptom_result && r.symptom_result.symptoms) {
      return r.symptom_result.symptoms.filter((s) => s && s !== '信息不足')
    }
  }
  return []
})
const currentConfidence = computed(() => {
  for (let i = messages.value.length - 1; i >= 0; i--) {
    const r = messages.value[i].response
    if (r && r.constitution_result && r.constitution_result.confidence !== undefined) {
      return r.constitution_result.confidence
    }
  }
  return 0
})
const latencySec = computed(() => {
  for (let i = messages.value.length - 1; i >= 0; i--) {
    const r = messages.value[i].response
    if (r && r.latency_sec !== undefined) return r.latency_sec
  }
  return null
})
const latencyTarget = computed(() => {
  for (let i = messages.value.length - 1; i >= 0; i--) {
    const r = messages.value[i].response
    if (r && r.latency_target_sec) return r.latency_target_sec
  }
  return 3
})
const latencyOk = computed(() => {
  for (let i = messages.value.length - 1; i >= 0; i--) {
    const r = messages.value[i].response
    if (r && r.latency_ok !== undefined) return r.latency_ok
  }
  return null
})
const latencyLabel = computed(() => {
  const v = latencySec.value
  return v !== null ? v + 's' : '--'
})

const confidenceColor = computed(() => {
  const c = currentConfidence.value
  if (c <= 0) return 'bg-gray-300'
  if (c < 0.6) return 'bg-red-500'
  if (c < 0.8) return 'bg-amber-500'
  return 'bg-green-500'
})
const confidenceColorText = computed(() => {
  const c = currentConfidence.value
  if (c <= 0) return 'text-gray-400'
  if (c < 0.6) return 'text-red-600'
  if (c < 0.8) return 'text-amber-600'
  return 'text-green-600'
})

const confidenceClass = (c) => {
  if (c < 0.6) return 'text-red-600'
  if (c < 0.8) return 'text-amber-600'
  return 'text-green-600'
}

const formatSymptomSummary = (s) => {
  if (!s) return '无'
  const parts = []
  if (s.symptoms && s.symptoms.length) parts.push(s.symptoms.join('、'))
  if (s.tongue && s.tongue !== '未采集') parts.push('舌：' + s.tongue)
  if (s.pulse && s.pulse !== '未采集') parts.push('脉：' + s.pulse)
  return parts.length ? parts.join('；') : '信息不足'
}

const formatSecondary = (sec) => {
  if (!sec) return '无'
  if (Array.isArray(sec)) return sec.length ? sec.join('、') : '无'
  return sec
}

const renderMd = (text) => {
  if (!text) return ''
  try {
    return marked.parse(String(text))
  } catch {
    return String(text)
  }
}

const scrollToBottom = async () => {
  await nextTick()
  if (scrollArea.value) scrollArea.value.scrollTop = scrollArea.value.scrollHeight
}

const autoResize = () => {
  nextTick(() => {
    const el = inputArea.value
    if (!el) return
    el.style.height = 'auto'
    el.style.height = Math.min(el.scrollHeight, 128) + 'px'
  })
}

const showMiniToastFor = (text, ms = 2500) => {
  miniToast.value = text
  setTimeout(() => {
    if (miniToast.value === text) miniToast.value = ''
  }, ms)
}

const send = async () => {
  const text = userInput.value.trim()
  if (!text || store.loading) return
  userInput.value = ''
  autoResize()
  try {
    await store.sendMessage(text)
  } catch (err) {
    const msg = (err && err.userMessage) || (err && err.message) || '发送失败'
    const code = (err && err.status) || (store.error && store.error.code) || 'chat_error'
    emit('error', msg, code)
  } finally {
    await scrollToBottom()
  }
}

const reset = async () => {
  if (store.loading) return
  try {
    await store.reset()
  } finally {
    userInput.value = ''
    autoResize()
  }
}

const fetchTools = async () => {
  try {
    const res = await axios.get('/api/agents/tools')
    toolsMode.value = res.data.mode || 'local'
  } catch (err) {
    toolsMode.value = 'local'
  }
}

onMounted(async () => {
  fetchTools()
  nextTick(() => inputArea.value && inputArea.value.focus())

  if (props.skipRestore) {
    // mini 模式父组件已经 seed 过，不需要再恢复
    await scrollToBottom()
    return
  }

  // 如果 store 里有上次会话，先渲染本地缓存给用户即时看到
  if (store.hasSession) {
    await scrollToBottom()
    restoring.value = true
    if (props.mode === 'page') restoreHint.value = '正在从后端恢复会话...'
    const result = await store.restoreFromBackend()
    restoring.value = false
    let hint = ''
    if (result.source === 'backend') {
      hint = `已从后端恢复 ${result.count} 条消息`
    } else if (result.stale) {
      hint = '后端会话已过期，使用本地缓存'
    } else if (result.error) {
      hint = '后端连接异常，使用本地缓存'
    }
    if (hint) {
      if (props.mode === 'page') {
        restoreHint.value = hint
        setTimeout(() => {
          if (restoreHint.value === hint) restoreHint.value = ''
        }, 3500)
      } else {
        showMiniToastFor(hint, 2500)
      }
    }
    if (result.restored) await scrollToBottom()
  }
})
</script>

<style scoped>
.md-content :deep(p) {
  margin: 0.25rem 0;
}
</style>
