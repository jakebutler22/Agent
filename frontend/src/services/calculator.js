const supportedOperations = new Set(['add', 'subtract', 'multiply', 'divide'])

export async function requestCalculation({ operation, a, b }) {
  if (!supportedOperations.has(operation)) {
    throw new Error('Choose a supported operation.')
  }

  const query = new URLSearchParams({ a: String(a), b: String(b) })
  let response

  try {
    response = await fetch(`/api/${operation}?${query}`)
  } catch {
    throw new Error('Unable to reach the calculator service.')
  }

  let payload

  try {
    payload = await response.json()
  } catch {
    throw new Error('The calculator service returned an invalid response.')
  }

  if (!response.ok) {
    throw new Error(typeof payload.detail === 'string' ? payload.detail : 'The calculation failed.')
  }

  if (typeof payload.result !== 'number') {
    throw new Error('The calculator service returned an invalid result.')
  }

  return payload.result
}

