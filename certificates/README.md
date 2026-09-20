# Certificates

Keep verified certificates here, and only certificates you actually hold.

1. Add the file (PDF or PNG) to this folder, e.g. `certificates/course-name.pdf`.
2. Add an entry to `certifications` in [`data/profile.json`](../data/profile.json):

   ```json
   {
     "name": "Exact certificate title",
     "issuer": "Issuing organisation",
     "year": 2026,
     "url": "https://verification-link-from-the-issuer"
   }
   ```

3. Run `python scripts/update_readme.py` (or wait for the Profile update workflow).

A public verification link from the issuer is better than a screenshot. Do not upload documents that
contain a government ID number, date of birth or home address.
