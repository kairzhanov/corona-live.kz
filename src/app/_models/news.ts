import { NewsType } from '../_enums/news.enum';
import { City } from './city';
import { Tag } from './tag';

export class News {
    id: number;
    title: string;
    description: string;
    link: string;
    date: Date;
    type: NewsType;
    city: City[];
    tags: Tag[]
}
