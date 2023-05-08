from .spectra_reader import SpectraReader
import scipy.io as sio

class MatReader(SpectraReader):
    def __init__(self, base_dir, json_dir, filename_func, struct_name, wavelengths_struct=None):
        super().__init__(base_dir, json_dir, filename_func)
        self.struct_name = struct_name
        self.wavelengths_struct_name = wavelengths_struct
        self.wavelengths = None
        self.mat_file = None

    def load_data(self, sample_id):
        filename = self.filename_func(self.base_dir, sample_id)
        self.mat_file = sio.loadmat(filename)
        print("mat loaded")
        self.data = self.mat_file[self.struct_name]
        if self.wavelengths_struct_name:
            self.wavelengths = self.mat_file[self.wavelengths_struct_name]
            #print("shape")
            #print(self.wavelengths.shape)
        else:
            arr = self.get_spectrum(0,0) # get a pixel
            self.wavelengths = np.arange(arr.size)
        self.height, self.width, _ = self.data.shape
        #print("shape")
        #print(self.data.shape)
        #print(self.height)
        #print(self.width)
        super().load_data(sample_id)
        
    def set_base_dir(self, base_dir):
        self.base_dir = base_dir
        
    def get_numpy(self):
        return(self.data)
    
    def get_numpy_of(self, sname):
        return(self.mat_file[sname])
        
    def get_wavelengths(self):
        return self.wavelengths.flatten()

    def get_spectrum(self, x, y):
        if self.data is None:
            raise ValueError("Spectral data not loaded. Call load_data() first.")
        return self.data[y, x, :]
