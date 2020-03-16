import { Component, OnInit } from '@angular/core';
import { DataService } from './_services/data.service';
import { News } from './_models/news';
import { NewsType } from './_enums/news.enum';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit  {
  title = 'corona-live';
  news: News[] = [];

  constructor (private dataService: DataService) {}

  ngOnInit() {
    // this.getNews();
    this.getOfficialNews();
  }

  getOfficialNews() {
    this.dataService.getOfficialNews().subscribe(result => {
      console.log(result);
    }, error => {
      console.log(error);
    });
  }

  getNews(): void {
    this.dataService.getNews().subscribe(result => {
      this.news = result;
    }, error => {
      console.log("ERROR - connection problem");
      // alert("К сожалению, произошли проблемы при подключении к серверу, попробуйте позже");
    });
  }


}
