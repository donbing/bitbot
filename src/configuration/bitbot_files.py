from os.path import join as pjoin, exists
import errno
import os


def use_config_dir(base_config_path):
    return BitBotFiles(base_config_path)


class BitBotFiles():
    all_files = {}

    def __init__(self, base_path):
        self.base_path = base_path
        self.log_file_path = pjoin(base_path, 'logs/debug.log')

        self.config_folder = pjoin(base_path, 'config/')
        self.resource_folder = pjoin(base_path, 'src/resources')
        self.photos_folder = pjoin(base_path, 'pictures/')

        os.makedirs(self.photos_folder, exist_ok=True)

        self.config_ini = self.existing_file_path('config.ini')
        self.logging_ini = self.existing_file_path('logging.ini')

        self.base_style = self.load_mpl_style('base.mplstyle')
        self.volume_style = self.load_mpl_style('volume.mplstyle')
        self.small_screen_style = self.load_mpl_style('small.mplstyle')
        self.expanded_style = self.load_mpl_style('default.expanded.mplstyle')
        self.small_expanded_style = self.load_mpl_style('small.expanded.mplstyle')

    def load_mpl_style(self, file_name):
        file_path = pjoin(self.config_folder, 'mpl_styles', file_name)
        if not exists(file_path):
            self.file_not_found(file_path)
        self.all_files[file_name] = file_path
        return file_path
            
    def existing_file_path(self, file_name):
        file_path = pjoin(self.config_folder, file_name)
        if not exists(file_path):
            self.file_not_found(file_path)
        self.all_files[file_name] = file_path
        return file_path

    def file_not_found(self, file_path):
        raise FileNotFoundError(
                errno.ENOENT,
                os.strerror(errno.ENOENT),
                file_path)

    def files_ending_with(self, ending):
        return list(
            filter(lambda f: f.endswith(ending), self.all_files.keys())
        )

    def __repr__(self):
        return f'<Bitbot config files:{str(self.base_path)}>'
