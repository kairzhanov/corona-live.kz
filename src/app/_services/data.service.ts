import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { News } from '../_models/news';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class DataService {

  constructor(private http: HttpClient) { }

  getNews(): Observable<News[]> {
    return this.http.get<News[]>(`${environment.apiUrl}/news`);
  }

  getOfficialNews() {
    return this.http.get("http://www.gov.kz/api/v1/public/content-manager/news?sort-by=created_date:DESC&projects=eq:dsm&page=1&size=10");
  }
}
