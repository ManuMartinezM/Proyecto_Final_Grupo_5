from fastapi import FastAPI
import trips_discount_model

analyze_for_discount = trips_discount_model.train()

app = FastAPI()

# /discount/?pu_location=123123&do_location=1231231&day=20&hour=14


@app.get('/discount')
def is_discount_applicable(pu_location: int, do_location: int, day: int, hour: int, year: int = 2023, month: int = 6):
    if analyze_for_discount(pu_location, do_location, year, month, day, hour):
        return True
    else:
        return False
