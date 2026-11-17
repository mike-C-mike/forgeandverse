(() => {
  'use strict';
  const distance = document.querySelector('[data-material-distance-demo]');
  if (distance) {
    const controls = distance.querySelector('[data-material-distance-controls]');
    const data = {
      close: {
        kicker:'Close view',
        heading:'The full message matters.',
        copy:'Up close, the title, supporting words, and finer details can work together. The question is whether the entire composition rewards a deliberate reading.',
        principle:'Preserve legible supporting text and the relationships between its elements.'
      },
      across: {
        kicker:'Across the room',
        heading:'Hierarchy carries the idea.',
        copy:'At a glance from farther away, the strongest headline and overall contrast may register before smaller supporting language. The piece needs a clear visual order.',
        principle:'Give the main line enough prominence without sacrificing the work when seen close.'
      },
      passing: {
        kicker:'In passing',
        heading:'The silhouette speaks first.',
        copy:'During a brief glance, a viewer is more likely to notice shape, contrast, and a focal point than fine text. Recognition comes before reading.',
        principle:'Let the composition communicate before asking someone to stop and read.'
      }
    };
    const buttons = [...distance.querySelectorAll('[data-distance-choice]')];
    const kicker = distance.querySelector('[data-distance-kicker]');
    const heading = distance.querySelector('[data-distance-heading]');
    const description = distance.querySelector('[data-distance-description]');
    const principle = distance.querySelector('[data-distance-principle]');
    const apply = (key) => {
      if (!Object.prototype.hasOwnProperty.call(data,key)) return;
      const item=data[key];
      distance.dataset.distance=key;
      buttons.forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.distanceChoice===key)));
      if(kicker) kicker.textContent=item.kicker;
      if(heading) heading.textContent=item.heading;
      if(description) description.textContent=item.copy;
      if(principle) principle.textContent=item.principle;
    };
    buttons.forEach(b=>b.addEventListener('click',()=>apply(b.dataset.distanceChoice)));
    if(controls) controls.hidden=false;
    apply('close');
  }

  const finishes = document.querySelector('[data-material-finish-demo]');
  if (finishes) {
    const controls=finishes.querySelector('[data-material-finish-controls]');
    const finishButtons=[...finishes.querySelectorAll('[data-finish-choice]')];
    const lightButtons=[...finishes.querySelectorAll('[data-light-choice]')];
    const kicker=finishes.querySelector('[data-finish-kicker]');
    const heading=finishes.querySelector('[data-finish-heading]');
    const description=finishes.querySelector('[data-finish-description]');
    const principle=finishes.querySelector('[data-finish-principle]');
    const names={ matte:'Matte', satin:'Satin', gloss:'Gloss' };
    const lights={ indirect:'Soft indirect lighting', window:'Facing window', spot:'Overhead spot' };
    const messages={
      matte:{
        indirect:['Diffuse, subdued light.','A low-sheen surface tends to scatter reflected light rather than form sharp reflections. It can look restrained under soft room lighting.'],
        window:['Reflections are more diffuse.','Facing a bright window may still produce a pale region, even if there is not a sharply defined mirror image. Placement still matters.'],
        spot:['A soft highlight can remain.','A matte surface can spread a spot reflection over a broader area, but this does not eliminate every distracting highlight.']
      },
      satin:{
        indirect:['A balance of surface and sheen.','With softer light, a modest sheen may preserve a sense of depth without drawing much attention to reflected light.'],
        window:['Some reflection remains.','A moderate sheen may show a window reflection while preserving much of the underlying composition. Placement and viewing angle still matter.'],
        spot:['A visible highlight may compete.','An overhead light can create a noticeable highlight on some satin finishes, depending on coating and viewing angle.']
      },
      gloss:{
        indirect:['Depth with more reflectivity.','A reflective finish can emphasize contrast and rich dark tones in gentle lighting, though the result varies by print and coating.'],
        window:['The window can become part of the picture.','A more defined window reflection may cross the text or focal point and compete with what the artwork is trying to communicate.'],
        spot:['Bright, concentrated glare is possible.','Strong overhead lighting can create a pronounced highlight that obscures details where the light reflects toward the viewer.']
      }
    };
    const questions={
      indirect:'Is the surface calm enough to let the work lead?',
      window:'Will a reflection cross the part of the artwork a viewer needs to read?',
      spot:'Where would a bright highlight fall from a normal viewing position?'
    };
    const apply=()=>{
      const finish=finishes.dataset.finish;
      const light=finishes.dataset.light;
      if(!messages[finish]||!messages[finish][light]) return;
      const [title,copy]=messages[finish][light];
      finishButtons.forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.finishChoice===finish)));
      lightButtons.forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.lightChoice===light)));
      if(kicker) kicker.textContent=names[finish]+' finish · '+lights[light];
      if(heading) heading.textContent=title;
      if(description) description.textContent=copy;
      if(principle) principle.textContent=questions[light];
    };
    finishButtons.forEach(b=>b.addEventListener('click',()=>{finishes.dataset.finish=b.dataset.finishChoice;apply();}));
    lightButtons.forEach(b=>b.addEventListener('click',()=>{finishes.dataset.light=b.dataset.lightChoice;apply();}));
    if(controls) controls.hidden=false;
    apply();
  }
})();