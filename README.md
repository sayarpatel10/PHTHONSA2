# ShopImpact — Conscious Shopping Dashboard

A Python and Streamlit web app for the Year 1 Python Programming Summative Assessment.

## Project overview

ShopImpact helps users become more aware of their shopping habits. Users can record purchases, see a simplified estimated CO₂ impact, review monthly spending, earn badges, and explore greener alternatives.

## Features

- Add a purchase with product type, brand/store, price, date, and an ethical-choice checkbox.
- Instantly estimate CO₂ impact using **price × product-category multiplier**.
- View monthly spending, estimated impact, number of purchases, and ethical choices.
- View badges such as Eco Saver, Low Impact Shopper, Second-hand Star, Ethical Choice Champion, and Mindful Planner.
- See greener brand/seller ideas, greener alternatives, and random eco tips.
- Review purchase history, download it as a CSV file, and remove an entry.
- Switch between Light and Dark modes. Form fields, dropdown menus, options, and text use high-contrast colors in both modes.
- Uses Python lists, dictionaries, functions, loops, conditionals, `datetime`, pandas, and Streamlit.
- Includes a separate desktop Turtle graphics program.

## Files

- `app.py` — main Streamlit application.
- `requirements.txt` — Python packages needed by Streamlit Cloud.
- `turtle_graphics.py` — desktop Turtle drawing of a leaf and footprint.
- `README.md` — project information and deployment steps.

## CO₂ estimate note

The assignment asks for an estimate using price multiplied by a product multiplier. The multipliers in this project are simplified classroom values. They are not verified life-cycle assessment data and should not be presented as exact emissions for a real product.

## Run the app on your computer

1. Install Python 3.10 or newer.
2. Open a terminal in this project folder.
3. Install the packages:

   ```bash
   pip install -r requirements.txt
   ```

4. Start Streamlit:

   ```bash
   streamlit run app.py
   ```

5. Streamlit will open the website in your browser.

## Turtle graphics

To run the desktop Turtle illustration locally:

```bash
python turtle_graphics.py
```

This opens a separate Turtle window. Streamlit Cloud runs without a desktop GUI, so the web app displays a cloud-safe leaf illustration instead of trying to open a Turtle window.

## GitHub and Streamlit Cloud deployment

1. Create a GitHub repository with the name required by your teacher, for example `IDAI102-YourStudentID-YourName`.
2. Upload `app.py`, `requirements.txt`, `README.md`, and `turtle_graphics.py` to the root of the repository.
3. Open [Streamlit Community Cloud](https://share.streamlit.io/).
4. Sign in with GitHub and choose **Create app** / **Deploy an app**.
5. Select your repository, branch, and `app.py` as the main file.
6. Deploy the app and wait for the build to finish.
7. Copy the live app URL and add it to this README and your submission document.
8. Follow your school's instruction to provide repository access to `ai.assignments@wacpinternational.org`.

## Testing checklist

- [ ] Add a low-price purchase.
- [ ] Add a high-price purchase.
- [ ] Add a second-hand item and check the badge.
- [ ] Add at least three ethical choices and check the badge.
- [ ] Check that monthly totals update after saving.
- [ ] Switch Light → Dark → Light and inspect every dropdown, input, label, and button.
- [ ] Download the CSV history.
- [ ] Remove a purchase and confirm the totals update.
- [ ] Test the deployed app on a phone-sized screen.

## Student details to complete

- Student name: [Enter your full name]
- Candidate registration number: [Enter your number]
- School: [Enter your school name]
- Live Streamlit app URL: [Paste after deployment]
- GitHub repository URL: [Paste after creating the repository]
