import flet as ft
import requests

def main(page: ft.Page):
    def get_exchange_rates(base_currency):
        url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"
        response = requests.get(url)
        data = response.json()
        return data['rates']

    def open_banner(text):
        b_text.value = text
        page.open(banner)
        page.update()

    def close_banner(e):
        page.close(banner)
        page.update()

    def convert(e):
        d1_value = d1.value
        d2_value = d2.value

        if d1_value is None or d2_value is None:
            open_banner("Выберите обе валюты!")
        elif d1_value == d2_value:
            open_banner("Выбраны одинаковые валюты!")
        else:
            try:
                rates = get_exchange_rates(d1_value)
                print(rates[d2_value])
                converted_amount = float(tf.value) * rates[d2_value]

                symbols = {
                    "RUB": "₽",
                    "USD": "$",
                    "EUR": "€",
                    "UAH": "₴",
                    "PLN": "zł",
                    "MDL": "MDL"
                }

                t.value = f"Сумма в {symbols[d2_value]}: {converted_amount:.2f}"

                if banner.open == True:
                    close_banner(e=None)

            except ValueError:
                open_banner("Введите корректную сумму!")

        page.update()

    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.title = "Конвертер валют"

    b_text = ft.Text("", color=ft.colors.BLACK)
    banner = ft.Banner(
            bgcolor=ft.colors.AMBER_100,
            leading=ft.Icon(ft.icons.WARNING_AMBER_ROUNDED, color=ft.colors.AMBER, size=40),
            content=b_text,
            actions=[ft.TextButton(text="Ok", on_click=close_banner, style=ft.ButtonStyle(color=ft.colors.BLUE))]
        )

    d1 = ft.Dropdown(options=[
            ft.dropdown.Option("USD"),
            ft.dropdown.Option("RUB"),
            ft.dropdown.Option("UAH"),
            ft.dropdown.Option("PLN"),
            ft.dropdown.Option("EUR"),
            ft.dropdown.Option("MDL"),
        ])
    
    d2 = ft.Dropdown(options=[
            ft.dropdown.Option("USD"),
            ft.dropdown.Option("RUB"),
            ft.dropdown.Option("UAH"),
            ft.dropdown.Option("PLN"),
            ft.dropdown.Option("EUR"),
            ft.dropdown.Option("MDL"),
        ])

    t = ft.Text("", size=20)
    tf = ft.TextField(label="Сумма", icon=ft.icons.MONETIZATION_ON, width=500)

    page.add(ft.Text("Конвертер валют", size=30))
    page.add(ft.Divider())
    page.add(
        ft.ResponsiveRow(
            [
            d1,
            ft.Icon(ft.icons.ARROW_CIRCLE_DOWN),
            d2,
            ],
        width=500)
    )
    page.add(ft.Text("Введите сумму:"))
    page.add(tf)
    page.add(ft.ElevatedButton(icon=ft.icons.LINE_AXIS, text="Конвертировать", on_click=convert))
    page.add(t)

ft.app(main)
