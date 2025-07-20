// Test script for interaction warnings
import { checkInteractions, checkDoseWarnings, checkSynergies } from './interactions'

// Test data
const testMedications = [
  { id: 'levo1', name: 'Levotiroxina 100mcg' },
  { id: 'metf1', name: 'Metformina 850mg' }
]

const testSupplements = [
  {
    id: 'fiber_supplement',
    name: 'Fibra Dietaria (Psyllium, Inulina, Salvado de avena)',
    custom_dose: '15g',
    servings: 1
  },
  {
    id: 'magnesium_supplement',
    name: 'Magnesio (Citrato, Bisglicinato, Malato)',
    custom_dose: '600mg',
    servings: 1
  },
  {
    id: 'vitamin_c_supplement',
    name: 'Vitamina C',
    custom_dose: '3000mg',
    servings: 1
  },
  {
    id: 'collagen_hydrolyzed',
    name: 'Colágeno Hidrolizado',
    servings: 1
  }
]

// Run tests
console.log('=== TESTING INTERACTIONS ===')
const interactions = checkInteractions(testMedications, testSupplements)
console.log('Interactions found:', interactions.length)
interactions.forEach(int => {
  console.log(`- ${int.medication} + ${int.supplement}:`)
  console.log(`  Severity: ${int.interaction.severity}`)
  console.log(`  Recommendation: ${int.interaction.recommendation}`)
})

console.log('\n=== TESTING DOSE WARNINGS ===')
const doseWarnings = checkDoseWarnings(testSupplements)
console.log('Dose warnings found:', doseWarnings.length)
doseWarnings.forEach(warning => {
  console.log(`- ${warning.supplement}: ${warning.current_dose} > ${warning.max_dose}`)
  if (warning.side_effect) {
    console.log(`  Side effect: ${warning.side_effect}`)
  }
})

console.log('\n=== TESTING SYNERGIES ===')
const synergies = checkSynergies(testSupplements)
console.log('Synergies found:', synergies.length)
synergies.forEach(synergy => {
  console.log(`- ${synergy.benefit}`)
  if (synergy.recommendation) {
    console.log(`  Recommendation: ${synergy.recommendation}`)
  }
})

console.log('\n=== TEST COMPLETE ===')