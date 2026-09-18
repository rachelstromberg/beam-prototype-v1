export const priorities = [
 {id:'concerns',title:'Catch consequential concerns',evidence:'7 of the 14 reports about safeguarding flags, mixed-up names, or missing risk details came with 4–5-star ratings.',action:['Prioritize checks for safeguarding flags, names, and risk details in quality evaluations.','Use verified examples from reported concerns to test prompt improvements.'],measure:['Confirmed consequential errors per 100 audited notes.','Percentage of reported concerns with a documented review outcome.']},
 {id:'templates',title:'Improve weaker templates',evidence:'Early Help, Mental Health, and Housing have the lowest average user ratings. Explore their feedback to identify what to test in a prompt-improvement pilot.',action:['Start with Early Help; assess Mental Health and Housing alongside it.','Pilot prompt revisions with practitioners.'],measure:['Percentage of notes passing a practitioner accuracy checklist.','Median minutes spent correcting each note.']},
 {id:'waits',title:'Make longer waits predictable',evidence:'Longer transcripts take longer in this sample. Waiting estimates should account for slower attempts as well as typical ones.',action:['Test length-aware waiting estimates.','Test leaving the page and returning to a completed note.'],measure:['Percentage of staff reporting that the wait interrupted their next task.','Percentage of those leaving who successfully return to a completed note.']},
 {id:'recovery',title:'Investigate incomplete work',evidence:'',action:['Investigate failed attempts and confirm which in-progress jobs are genuinely stuck.','Use the findings to improve failure messages and recovery paths.'],measure:['Percentage of failed attempts successfully recovered.','Median time from failure to a usable note.']}
];
export const questions=[
 ['Where does quality break down?','Which errors create the greatest risk or most extra editing?'],
 ['Do waits disrupt work?','When do waits interrupt the next task or cause staff to abandon a note?'],
 ['Why does work fail?','What causes failed attempts, and which recovery paths get staff back to a usable note?']
];
