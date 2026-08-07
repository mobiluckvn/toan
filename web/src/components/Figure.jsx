import React from 'react';
import { figureSrc } from '../lib/content.js';

export default function Figure({ fig }) {
  if (!fig) return null;
  return (
    <figure className="my-3.5">
      <img src={figureSrc(fig)} alt={fig.caption || 'hình minh hoạ'} loading="lazy"
           className="w-full rounded-xl border border-line bg-[#F8FBFD]" />
      {fig.caption && (
        <figcaption className="mt-1.5 text-center text-[12.5px] leading-relaxed text-mute">
          {fig.caption}
        </figcaption>
      )}
    </figure>
  );
}
