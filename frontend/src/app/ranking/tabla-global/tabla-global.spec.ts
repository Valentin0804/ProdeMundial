import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TablaGlobal } from './tabla-global';

describe('TablaGlobal', () => {
  let component: TablaGlobal;
  let fixture: ComponentFixture<TablaGlobal>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [TablaGlobal],
    }).compileComponents();

    fixture = TestBed.createComponent(TablaGlobal);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
