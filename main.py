import time

from mod_functions import base_url, base_query, get_soup, is_captcha_page, extract_company_name, \
    extract_company_location, extract_company_salary, extract_job_description, extract_job_posting_date, write_to_file, \
    data_file, check_next_page_status, sleep_time


def main():
    page_num = 0
    page_status = True
    echec_connexion = 1

    while page_status:
        active_page = base_url + base_query + str(page_num)
        active_page_soup = get_soup(active_page)
        captcha = is_captcha_page(active_page_soup)
        if active_page_soup and captcha is False:
            page_job_name_list = extract_company_name(active_page_soup)
            page_job_location_list = extract_company_location(active_page_soup)
            page_job_salary_list = extract_company_salary(active_page_soup)
            page_job_desc_list = extract_job_description(active_page_soup)
            page_job_post_date = extract_job_posting_date(active_page_soup)
            write_to_file(data_file, page_job_name_list, page_job_location_list, page_job_salary_list,
                          page_job_desc_list, page_job_post_date)
            print("Les annonces de la paginnation {} scrappées.".format(page_num))
            page_num = page_num + 10
            next_query = base_query + str(page_num)
            page_status = check_next_page_status(active_page, next_query)
        elif echec_connexion == 2:
            print("{} échecs de connexion au site, arrêt du script. Veuillez vérifierou mettre à jour le script. "
                  "Bye bye...".format(echec_connexion))
            exit()
        else:
            echec_connexion = echec_connexion + 1
            print("Échec de connexion au site. Nouvelle tentative de connexion dans {} seconde(s)".format(sleep_time))
            time.sleep(sleep_time)


if __name__ == '__main__':
    main()
