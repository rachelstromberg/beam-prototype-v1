export const priorities = [
  {
    id: 'support', nav: 'Target support where ratings are lower',
    title: 'Review what staff need from Early Help, Mental Health, and Housing notes.',
    evidence: 'These workflows have the three lowest average ratings in this sample.',
    council: 'Review notes with staff and document recurring corrections and missing information.',
    beam: 'Test template improvements based on customer feedback.',
    measure: ['Track editing minutes per note.', 'Track the percentage of reviewed notes that meet an agreed accuracy and completeness checklist.'],
  },
  {
    id: 'accuracy', nav: 'Look beyond ratings',
    title: 'High ratings can still carry accuracy concerns.',
    evidence: '7 of 14 reports of potentially consequential errors came with 4–5 stars.',
    council: 'Establish a simple way for staff to report inaccuracies, whatever their overall rating.',
    beam: 'Investigate recurring inaccuracies reported by customers.',
    measure: ['Track the percentage of reviewed notes with a confirmed error involving names or risk.'],
  },
  {
    id: 'waits', nav: 'Set expectations for generation time',
    title: 'Longer recordings mean longer generation times.',
    evidence: '',
    council: 'Check whether waiting interrupts staff’s work.',
    beam: 'If waiting is disruptive, trial leaving the screen and returning when results are ready.',
    measure: ['Track how often staff say waiting interrupted their work.'],
  },
];
