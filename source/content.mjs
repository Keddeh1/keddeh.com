import core from './content-core.mjs';
import services from './content-services.mjs';
import products from './content-products.mjs';
import architecture from './content-architecture.mjs';
import research from './content-research.mjs';
import foundries from './content-foundries.mjs';
import technology from './content-technology.mjs';
export const pages=[core,services,products,architecture,research,foundries,technology].flat();
export const pageByPath=new Map(pages.map(p=>[p.path,p]));
