<script setup>
import { ref } from 'vue'

import { requestCalculation } from './services/calculator'

const firstValue = ref('')
const secondValue = ref('')
const operation = ref('add')
const result = ref(null)
const errorMessage = ref('')
const isCalculating = ref(false)

const operations = [
  { value: 'add', label: 'Add (+)' },
  { value: 'subtract', label: 'Subtract (−)' },
  { value: 'multiply', label: 'Multiply (×)' },
  { value: 'divide', label: 'Divide (÷)' },
]

async function calculate() {
  const a = Number(firstValue.value)
  const b = Number(secondValue.value)

  result.value = null
  errorMessage.value = ''

  if (firstValue.value === '' || secondValue.value === '' || !Number.isFinite(a) || !Number.isFinite(b)) {
    errorMessage.value = 'Enter two valid numbers.'
    return
  }

  isCalculating.value = true

  try {
    result.value = await requestCalculation({ operation: operation.value, a, b })
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : 'The calculation failed.'
  } finally {
    isCalculating.value = false
  }
}
</script>

<template>
  <main class="page-shell">
    <section class="calculator-card" aria-labelledby="calculator-title">
      <header class="calculator-header">
        <p class="eyebrow">Hello Agent</p>
        <h1 id="calculator-title">Calculator</h1>
        <p>Choose an operation and let the backend handle the arithmetic.</p>
      </header>

      <form class="calculator-form" @submit.prevent="calculate">
        <div class="field">
          <label for="first-value">First number</label>
          <input
            id="first-value"
            v-model="firstValue"
            inputmode="decimal"
            name="first-value"
            placeholder="12"
            step="any"
            type="number"
          />
        </div>

        <div class="field">
          <label for="operation">Operation</label>
          <select id="operation" v-model="operation" name="operation">
            <option v-for="item in operations" :key="item.value" :value="item.value">
              {{ item.label }}
            </option>
          </select>
        </div>

        <div class="field">
          <label for="second-value">Second number</label>
          <input
            id="second-value"
            v-model="secondValue"
            inputmode="decimal"
            name="second-value"
            placeholder="3"
            step="any"
            type="number"
          />
        </div>

        <button type="submit" :disabled="isCalculating">
          {{ isCalculating ? 'Calculating…' : 'Calculate' }}
        </button>
      </form>

      <div class="status-grid" aria-live="polite">
        <section class="status-panel result-panel" aria-labelledby="result-title">
          <h2 id="result-title">Result</h2>
          <output>{{ result ?? '—' }}</output>
        </section>

        <section class="status-panel error-panel" aria-labelledby="error-title">
          <h2 id="error-title">Error</h2>
          <p role="alert">{{ errorMessage || 'None' }}</p>
        </section>
      </div>
    </section>
  </main>
</template>

<style scoped>
.page-shell {
  display: grid;
  min-height: 100vh;
  place-items: center;
  padding: 2rem 1rem;
}

.calculator-card {
  width: min(100%, 48rem);
  padding: clamp(1.5rem, 5vw, 3rem);
  border: 1px solid #ded5c8;
  border-radius: 1.5rem;
  background: #fffdf9;
  box-shadow: 0 1.5rem 4rem rgb(69 45 28 / 12%);
}

.calculator-header {
  max-width: 36rem;
  margin-bottom: 2rem;
}

.eyebrow {
  margin-bottom: 0.5rem;
  color: #a63f18;
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.14em;
  text-transform: uppercase;
}

h1 {
  color: #2e241d;
  font-size: clamp(2.25rem, 8vw, 4rem);
  font-weight: 750;
  letter-spacing: -0.05em;
  line-height: 1;
}

.calculator-header > p:last-child {
  margin-top: 1rem;
  color: #6f6258;
  font-size: 1.05rem;
}

.calculator-form {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
}

.field {
  display: grid;
  gap: 0.45rem;
}

label,
h2 {
  color: #4b3d33;
  font-size: 0.8rem;
  font-weight: 700;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}

input,
select {
  width: 100%;
  min-height: 3.25rem;
  padding: 0.75rem 0.9rem;
  border: 1px solid #cfc2b5;
  border-radius: 0.75rem;
  color: #2e241d;
  background: #ffffff;
}

input:focus,
select:focus {
  border-color: #c45125;
  outline: 3px solid rgb(196 81 37 / 20%);
}

button {
  min-height: 3.25rem;
  padding: 0.75rem 1.25rem;
  border: 0;
  border-radius: 0.75rem;
  color: #ffffff;
  background: #c45125;
  cursor: pointer;
  font-weight: 700;
  transition:
    background-color 160ms ease,
    transform 160ms ease;
}

button:hover:not(:disabled) {
  background: #963a18;
  transform: translateY(-1px);
}

button:focus-visible {
  outline: 3px solid rgb(196 81 37 / 30%);
  outline-offset: 3px;
}

button:disabled {
  cursor: wait;
  opacity: 0.65;
}

.status-grid {
  display: grid;
  gap: 1rem;
  margin-top: 1.5rem;
}

.status-panel {
  min-height: 7rem;
  padding: 1rem;
  border-radius: 0.9rem;
}

.result-panel {
  border: 1px solid #d3c5b8;
  background: #f6efe6;
}

.result-panel output {
  display: block;
  margin-top: 0.35rem;
  color: #2e241d;
  font-size: 2rem;
  font-weight: 750;
  overflow-wrap: anywhere;
}

.error-panel {
  border: 1px solid #edc9bc;
  background: #fff2ed;
}

.error-panel p {
  margin-top: 0.5rem;
  color: #922f12;
}

@media (min-width: 42rem) {
  .calculator-form {
    grid-template-columns: 1fr 0.9fr 1fr;
  }

  .calculator-form button {
    grid-column: 1 / -1;
  }

  .status-grid {
    grid-template-columns: 1fr 1fr;
  }
}
</style>

