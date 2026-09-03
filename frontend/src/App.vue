<script setup>
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'

import { requestCalculation } from './services/calculator'

const MAX_DISPLAY_LENGTH = 12
const MAX_HISTORY_LENGTH = 3

const operationSymbols = {
  add: '+',
  subtract: '−',
  multiply: '×',
  divide: '÷',
}

const keys = [
  { action: 'backspace', label: 'Delete last digit', symbol: '⌫', variant: 'utility' },
  { action: 'clear', label: 'All clear', symbol: 'AC', variant: 'utility' },
  { action: 'percent', label: 'Percent', symbol: '%', variant: 'utility' },
  { action: 'operation', label: 'Divide', symbol: '÷', value: 'divide', variant: 'operator' },
  { action: 'digit', label: 'Seven', symbol: '7', value: '7', variant: 'number' },
  { action: 'digit', label: 'Eight', symbol: '8', value: '8', variant: 'number' },
  { action: 'digit', label: 'Nine', symbol: '9', value: '9', variant: 'number' },
  { action: 'operation', label: 'Multiply', symbol: '×', value: 'multiply', variant: 'operator' },
  { action: 'digit', label: 'Four', symbol: '4', value: '4', variant: 'number' },
  { action: 'digit', label: 'Five', symbol: '5', value: '5', variant: 'number' },
  { action: 'digit', label: 'Six', symbol: '6', value: '6', variant: 'number' },
  { action: 'operation', label: 'Subtract', symbol: '−', value: 'subtract', variant: 'operator' },
  { action: 'digit', label: 'One', symbol: '1', value: '1', variant: 'number' },
  { action: 'digit', label: 'Two', symbol: '2', value: '2', variant: 'number' },
  { action: 'digit', label: 'Three', symbol: '3', value: '3', variant: 'number' },
  { action: 'operation', label: 'Add', symbol: '+', value: 'add', variant: 'operator' },
  { action: 'sign', label: 'Toggle sign', symbol: '±', variant: 'number' },
  { action: 'digit', label: 'Zero', symbol: '0', value: '0', variant: 'number' },
  { action: 'decimal', label: 'Decimal point', symbol: '.', variant: 'number' },
  { action: 'equals', label: 'Equals', symbol: '=', variant: 'operator' },
]

const currentValue = ref('0')
const storedValue = ref(null)
const pendingOperation = ref('')
const expression = ref('')
const errorMessage = ref('')
const isCalculating = ref(false)
const waitingForOperand = ref(false)
const justCalculated = ref(false)
const calculationHistory = ref([])
let nextCalculationId = 1

const previousCalculations = computed(() => {
  const historyStart = justCalculated.value ? 1 : 0

  return calculationHistory.value
    .slice(historyStart, historyStart + MAX_HISTORY_LENGTH)
    .reverse()
})

function clearError() {
  errorMessage.value = ''
}

function formatNumber(value) {
  if (!Number.isFinite(value)) {
    return 'Error'
  }

  if (Object.is(value, -0)) {
    return '0'
  }

  return String(Number(value.toPrecision(12)))
}

function beginNewEntry(value) {
  currentValue.value = value
  waitingForOperand.value = false

  if (justCalculated.value) {
    expression.value = ''
    justCalculated.value = false
  }
}

function appendDigit(digit) {
  if (isCalculating.value) {
    return
  }

  clearError()

  if (waitingForOperand.value || justCalculated.value) {
    beginNewEntry(digit)
    return
  }

  if (currentValue.value === '0') {
    currentValue.value = digit
  } else if (currentValue.value === '-0') {
    currentValue.value = `-${digit}`
  } else if (currentValue.value.replace('-', '').replace('.', '').length < MAX_DISPLAY_LENGTH) {
    currentValue.value += digit
  }
}

function appendDecimal() {
  if (isCalculating.value) {
    return
  }

  clearError()

  if (waitingForOperand.value || justCalculated.value) {
    beginNewEntry('0.')
  } else if (!currentValue.value.includes('.')) {
    currentValue.value += '.'
  }
}

function clearCalculator() {
  if (isCalculating.value) {
    return
  }

  currentValue.value = '0'
  storedValue.value = null
  pendingOperation.value = ''
  expression.value = ''
  errorMessage.value = ''
  waitingForOperand.value = false
  justCalculated.value = false
}

function backspace() {
  if (isCalculating.value || waitingForOperand.value) {
    return
  }

  clearError()

  if (justCalculated.value) {
    expression.value = ''
    justCalculated.value = false
  }

  const shortenedValue = currentValue.value.slice(0, -1)
  currentValue.value = shortenedValue === '' || shortenedValue === '-' ? '0' : shortenedValue
}

function toggleSign() {
  if (isCalculating.value) {
    return
  }

  clearError()

  if (waitingForOperand.value || justCalculated.value) {
    beginNewEntry('-0')
    return
  }

  if (currentValue.value !== '0') {
    currentValue.value = currentValue.value.startsWith('-')
      ? currentValue.value.slice(1)
      : `-${currentValue.value}`
  }
}

function applyPercent() {
  if (isCalculating.value) {
    return
  }

  clearError()

  if (waitingForOperand.value) {
    beginNewEntry('0')
    return
  }

  currentValue.value = formatNumber(Number(currentValue.value) / 100)
  justCalculated.value = false
}

function selectOperation(operation) {
  if (isCalculating.value) {
    return
  }

  clearError()

  if (pendingOperation.value && waitingForOperand.value) {
    pendingOperation.value = operation
    expression.value = `${formatNumber(storedValue.value)}${operationSymbols[operation]}`
    return
  }

  const operand = Number(currentValue.value)

  if (!Number.isFinite(operand)) {
    errorMessage.value = 'Enter a valid number.'
    return
  }

  storedValue.value = operand
  pendingOperation.value = operation
  expression.value = `${formatNumber(operand)}${operationSymbols[operation]}`
  waitingForOperand.value = true
  justCalculated.value = false
}

async function calculate() {
  if (isCalculating.value) {
    return
  }

  if (!pendingOperation.value || storedValue.value === null) {
    errorMessage.value = 'Choose an operation first.'
    return
  }

  if (waitingForOperand.value) {
    errorMessage.value = 'Enter a second number.'
    return
  }

  const operation = pendingOperation.value
  const a = storedValue.value
  const b = Number(currentValue.value)

  if (!Number.isFinite(b)) {
    errorMessage.value = 'Enter a valid number.'
    return
  }

  const completedExpression = `${formatNumber(a)}${operationSymbols[operation]}${formatNumber(b)}`
  expression.value = completedExpression
  errorMessage.value = ''
  isCalculating.value = true

  try {
    const result = await requestCalculation({ operation, a, b })
    const formattedResult = formatNumber(result)

    currentValue.value = formattedResult
    calculationHistory.value = [
      {
        id: nextCalculationId,
        expression: completedExpression,
        result: formattedResult,
      },
      ...calculationHistory.value,
    ].slice(0, MAX_HISTORY_LENGTH)
    nextCalculationId += 1
    storedValue.value = null
    pendingOperation.value = ''
    waitingForOperand.value = false
    justCalculated.value = true
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : 'The calculation failed.'
  } finally {
    isCalculating.value = false
  }
}

function pressKey(key) {
  const actions = {
    backspace,
    clear: clearCalculator,
    decimal: appendDecimal,
    digit: () => appendDigit(key.value),
    equals: calculate,
    operation: () => selectOperation(key.value),
    percent: applyPercent,
    sign: toggleSign,
  }

  actions[key.action]?.()
}

function handleKeyboard(event) {
  if (/^\d$/.test(event.key)) {
    appendDigit(event.key)
  } else if (event.key === '.') {
    appendDecimal()
  } else if (event.key === 'Backspace') {
    backspace()
  } else if (event.key === 'Escape' || event.key.toLowerCase() === 'c') {
    clearCalculator()
  } else if (event.key === '%') {
    applyPercent()
  } else if (event.key === 'Enter' || event.key === '=') {
    calculate()
  } else if (event.key === '+') {
    selectOperation('add')
  } else if (event.key === '-') {
    selectOperation('subtract')
  } else if (event.key === '*' || event.key.toLowerCase() === 'x') {
    selectOperation('multiply')
  } else if (event.key === '/') {
    selectOperation('divide')
  } else {
    return
  }

  event.preventDefault()
}

onMounted(() => window.addEventListener('keydown', handleKeyboard))
onBeforeUnmount(() => window.removeEventListener('keydown', handleKeyboard))
</script>

<template>
  <main class="page-shell">
    <section class="calculator-frame" aria-labelledby="calculator-title">
      <h1 id="calculator-title" class="sr-only">Calculator</h1>

      <div class="calculator-toolbar" aria-hidden="true">
        <div class="window-controls">
          <span class="window-dot window-dot--red"></span>
          <span class="window-dot window-dot--yellow"></span>
          <span class="window-dot window-dot--dim"></span>
        </div>
      </div>

      <div class="calculator-display" aria-live="polite">
        <ol
          v-if="previousCalculations.length"
          class="calculation-history"
          aria-label="Recent calculations"
        >
          <li
            v-for="calculation in previousCalculations"
            :key="calculation.id"
            class="calculation-history__item"
            :aria-label="`${calculation.expression} equals ${calculation.result}`"
          >
            <span aria-hidden="true">{{ calculation.expression }}</span>
            <span class="calculation-history__equals" aria-hidden="true">=</span>
            <span class="calculation-history__result" aria-hidden="true">
              {{ calculation.result }}
            </span>
          </li>
        </ol>

        <p v-if="errorMessage" class="display-message display-message--error" role="alert">
          {{ errorMessage }}
        </p>
        <p v-else class="display-message">{{ expression || '\u00a0' }}</p>
        <output class="display-value" aria-label="Display">
          {{ isCalculating ? '…' : currentValue }}
        </output>
      </div>

      <div class="calculator-keypad" aria-label="Calculator keypad">
        <button
          v-for="key in keys"
          :key="`${key.action}-${key.value || key.symbol}`"
          class="calculator-key"
          :class="[
            `calculator-key--${key.variant}`,
            { 'is-selected': key.action === 'operation' && pendingOperation === key.value },
          ]"
          type="button"
          :aria-label="key.label"
          :aria-pressed="key.action === 'operation' ? pendingOperation === key.value : undefined"
          :disabled="isCalculating"
          @click="pressKey(key)"
        >
          <span aria-hidden="true">{{ key.symbol }}</span>
        </button>
      </div>
    </section>
  </main>
</template>

<style scoped>
.page-shell {
  display: grid;
  min-height: 100vh;
  place-items: center;
  padding: clamp(0.45rem, 3vw, 1.5rem);
}

.calculator-frame {
  width: min(100%, 29rem);
  padding: 0.75rem 1.15rem 1.2rem;
  overflow: hidden;
  border: 2px solid #666664;
  border-radius: clamp(2.35rem, 10vw, 3.6rem);
  background: #1c1c1c;
  box-shadow:
    0 1.75rem 4rem rgb(0 0 0 / 35%),
    inset 0 0 0 2px #101010,
    inset 0 1px 0 rgb(255 255 255 / 48%);
}

.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

.calculator-toolbar {
  display: flex;
  align-items: center;
  min-height: 5.1rem;
}

.window-controls {
  display: flex;
  gap: clamp(0.65rem, 2.6vw, 1.25rem);
  align-items: center;
  padding-left: clamp(0.35rem, 2vw, 1rem);
}

.window-dot {
  width: clamp(1.1rem, 6vw, 1.8rem);
  border: 1px solid rgb(255 255 255 / 8%);
  border-radius: 50%;
  aspect-ratio: 1;
  box-shadow: inset 0 -1px 2px rgb(0 0 0 / 25%);
}

.window-dot--red {
  background: #ff4050;
}

.window-dot--yellow {
  background: #ffc400;
}

.window-dot--dim {
  background: #454545;
}

.calculator-display {
  display: flex;
  min-height: 15rem;
  flex-direction: column;
  align-items: flex-end;
  justify-content: flex-end;
  padding: 0.25rem 0.2rem 1.15rem;
  text-align: right;
}

.calculation-history {
  display: grid;
  width: 100%;
  gap: 0.35rem;
  margin: 0 0 0.85rem;
  padding: 0;
  color: #99999d;
  font-size: clamp(0.9rem, 3.5vw, 1.1rem);
  font-variant-numeric: tabular-nums;
  list-style: none;
}

.calculation-history__item {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto minmax(4rem, auto);
  gap: 0.5rem;
  align-items: baseline;
}

.calculation-history__item > span:first-child {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.calculation-history__equals {
  color: #69696d;
}

.calculation-history__result {
  color: #cfcfd2;
}

.display-message {
  width: 100%;
  min-height: 2.9rem;
  overflow: hidden;
  color: #99999d;
  font-size: clamp(1.45rem, 8vw, 2.65rem);
  font-weight: 400;
  line-height: 1.1;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.display-message--error {
  color: #ff8b78;
  font-size: clamp(0.95rem, 4vw, 1.25rem);
}

.display-value {
  display: block;
  max-width: 100%;
  overflow: hidden;
  color: #f2f2f2;
  font-size: clamp(3rem, 14vw, 4.2rem);
  font-variant-numeric: tabular-nums;
  font-weight: 400;
  letter-spacing: -0.04em;
  line-height: 1.05;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.calculator-keypad {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: clamp(0.55rem, 2.6vw, 0.8rem);
}

.calculator-key {
  display: grid;
  min-width: 0;
  padding: 0;
  place-items: center;
  border: 1px solid rgb(255 255 255 / 20%);
  border-radius: 50%;
  aspect-ratio: 1;
  color: #f5f5f5;
  cursor: pointer;
  font-size: clamp(1.65rem, 9vw, 2.75rem);
  font-weight: 400;
  line-height: 1;
  box-shadow:
    inset 0 1px 1px rgb(255 255 255 / 10%),
    0 2px 2px rgb(0 0 0 / 30%);
  transition:
    background-color 120ms ease,
    color 120ms ease,
    transform 80ms ease;
  -webkit-tap-highlight-color: transparent;
}

.calculator-key:hover:not(:disabled) {
  filter: brightness(1.12);
}

.calculator-key:active:not(:disabled) {
  transform: scale(0.96);
}

.calculator-key:focus-visible {
  outline: 3px solid #ffffff;
  outline-offset: 3px;
}

.calculator-key:disabled {
  cursor: wait;
  opacity: 0.72;
}

.calculator-key--number {
  background: #4c4c4c;
}

.calculator-key--utility {
  background: #898989;
}

.calculator-key--operator {
  border-color: #ff9f0a;
  background: #ff9500;
  font-size: clamp(2rem, 10vw, 3.35rem);
  font-weight: 300;
}

.calculator-key--operator.is-selected {
  color: #ff9500;
  background: #ffffff;
}

@media (max-width: 24rem) {
  .calculator-frame {
    padding-inline: 0.8rem;
  }

  .calculator-toolbar {
    min-height: 4rem;
  }

  .calculator-display {
    min-height: 12.5rem;
  }
}
</style>
