import logging
from .default_webdriver import default_wd_func, default_wd_args, default_wd_kwargs


class WebDriverReanimator(object):

    def __init__(self, wd_func=default_wd_func, wd_args=default_wd_args,
            wd_kwargs=default_wd_kwargs, filename='session_id.txt'):
        self.webdriver = wd_func(*wd_args, **wd_kwargs)
        logging.debug('Opened new browser with session_id "{}"'.format(
                self.webdriver.session_id))
        self.filename = filename


    def __enter__(self):
        new_session_id = self.webdriver.session_id
        saved_session_id = self._load_session_id(self.filename)
        self.skip = self._validate_session_id(self.webdriver, saved_session_id)
        return self


    def __exit__(self, exc_type, exc_value, exc_tb):
        self._save_session_id(self.filename, self.webdriver.session_id)


    def _load_session_id(self, filename):
        try:
            with open(filename) as f:
                session_id = f.read()
            logging.debug('Loaded saved session_id "{}" from file "{}"'.format(
                    session_id, filename))
        except IOError:
            session_id = None
            logging.debug('Failed to load session_id from file "{}"'.format(
                    filename))
        return session_id


    def _save_session_id(self, filename, session_id):
        with open(filename, 'w') as f:
            f.write(session_id)
        logging.debug('Written session_id "{}" to file "{}"'.format(
                session_id, filename))


    def _validate_session_id(self, webdriver, saved_session_id):
        is_saved_session_id_valid = False
        new_session_id = webdriver.session_id
        try:
            if not saved_session_id:
                raise ValueError
            webdriver.session_id = saved_session_id

            # TODO: Come up with a more robust way
            #       to validate session_id.
            self.webdriver.find_element_by_xpath("//body")
            logging.debug(('Saved session_id "{}" is valid, ' \
                        + 'throwing the newly opened browser away').format(
                            saved_session_id))
            webdriver.session_id = new_session_id
            webdriver.close()
            webdriver.session_id = saved_session_id
            is_saved_session_id_valid = True
        except:
            logging.debug('Saved session_id "{}" is invalid'.format(
                    saved_session_id))
            logging.debug('Using the new browser with session_id "{}"'.format(
                    new_session_id))
            webdriver.session_id = new_session_id
        return is_saved_session_id_valid

