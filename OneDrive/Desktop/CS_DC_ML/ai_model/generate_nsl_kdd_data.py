"""
NSL-KDD Style Dataset Generator
Generates synthetic network traffic data for intrusion detection training
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
import random

class NSLKDDDataGenerator:
    def __init__(self, num_samples=50000):
        self.num_samples = num_samples
        self.feature_columns = [
            'duration', 'protocol_type', 'service', 'flag', 'src_bytes',
            'dst_bytes', 'land', 'wrong_fragment', 'urgent', 'hot',
            'num_failed_logins', 'logged_in', 'num_compromised', 'root_shell',
            'su_attempted', 'num_root', 'num_file_creations', 'num_shells',
            'num_access_files', 'num_outbound_cmds', 'is_host_login',
            'is_guest_login', 'count', 'srv_count', 'serror_rate',
            'srv_serror_rate', 'rerror_rate', 'srv_rerror_rate', 'same_srv_rate',
            'diff_srv_rate', 'srv_diff_host_rate', 'dst_host_count',
            'dst_host_srv_count', 'dst_host_same_srv_rate', 'dst_host_diff_srv_rate',
            'dst_host_same_src_port_rate', 'dst_host_srv_diff_host_rate',
            'dst_host_serror_rate', 'dst_host_srv_serror_rate', 'dst_host_rerror_rate',
            'dst_host_srv_rerror_rate'
        ]
        
        self.protocol_types = ['tcp', 'udp', 'icmp']
        self.services = ['http', 'ftp', 'smtp', 'ssh', 'telnet', 'dns', 'pop3', 'imap']
        self.flags = ['SF', 'REJ', 'RSTR', 'RSTO', 'SH', 'S1', 'S2', 'S3']
        
        self.attack_types = [
            'normal', 'neptune', 'satan', 'ipsweep', 'portsweep', 'teardrop', 
            'pod', 'smurf', 'land', 'back', 'buffer_overflow', 'warezclient',
            'warezmaster', 'imap', 'ftp_write', 'guess_passwd', 'multihop',
            'phf', 'spy', 'perl'
        ]
        
        self.attack_categories = {
            'normal': 'normal',
            'neptune': 'dos', 'teardrop': 'dos', 'pod': 'dos', 'smurf': 'dos', 'land': 'dos', 'back': 'dos',
            'buffer_overflow': 'u2r', 'warezmaster': 'u2r', 'perl': 'u2r', 'spy': 'u2r',
            'guess_passwd': 'r2l', 'ftp_write': 'r2l', 'imap': 'r2l', 'phf': 'r2l', 'multihop': 'r2l', 'warezclient': 'r2l',
            'satan': 'probe', 'ipsweep': 'probe', 'portsweep': 'probe', 'nmap': 'probe'
        }

    def generate_normal_traffic(self, num_samples):
        """Generate normal network traffic patterns"""
        data = []
        
        for _ in range(num_samples):
            # Normal traffic typically has reasonable values
            duration = np.random.exponential(100) if np.random.random() > 0.7 else 0
            protocol = np.random.choice(self.protocol_types, p=[0.8, 0.15, 0.05])
            service = np.random.choice(self.services, p=[0.4, 0.1, 0.1, 0.1, 0.05, 0.1, 0.05, 0.1])
            flag = np.random.choice(self.flags, p=[0.7, 0.05, 0.05, 0.05, 0.05, 0.02, 0.02, 0.06])
            
            src_bytes = np.random.lognormal(8, 1) if np.random.random() > 0.3 else 0
            dst_bytes = np.random.lognormal(7, 1) if np.random.random() > 0.4 else 0
            
            # Normal connections usually have low error rates
            serror_rate = np.random.beta(1, 10)
            rerror_rate = np.random.beta(1, 10)
            
            # Count features for normal traffic
            count = np.random.poisson(5)
            srv_count = np.random.poisson(3)
            
            same_srv_rate = np.random.beta(3, 2)
            diff_srv_rate = 1 - same_srv_rate
            
            # Host-level features
            dst_host_count = np.random.poisson(10)
            dst_host_srv_count = np.random.poisson(5)
            
            dst_host_same_srv_rate = np.random.beta(3, 2)
            dst_host_diff_srv_rate = 1 - dst_host_same_srv_rate
            
            dst_host_serror_rate = np.random.beta(1, 10)
            dst_host_rerror_rate = np.random.beta(1, 10)
            
            sample = [
                duration, protocol, service, flag, src_bytes, dst_bytes,
                0, 0, 0, np.random.poisson(0.5), 0, np.random.choice([0, 1], p=[0.3, 0.7]),
                0, 0, 0, 0, np.random.poisson(0.2), np.random.poisson(0.1),
                np.random.poisson(0.3), 0, 0, np.random.choice([0, 1], p=[0.8, 0.2]),
                count, srv_count, serror_rate, serror_rate, rerror_rate, rerror_rate,
                same_srv_rate, diff_srv_rate, np.random.beta(1, 5),
                dst_host_count, dst_host_srv_count, dst_host_same_srv_rate,
                1 - dst_host_same_srv_rate, np.random.beta(1, 5), np.random.beta(1, 5),
                dst_host_serror_rate, dst_host_serror_rate, dst_host_rerror_rate,
                dst_host_rerror_rate
            ]
            
            data.append(sample)
        
        return data

    def generate_attack_traffic(self, num_samples):
        """Generate attack traffic patterns"""
        data = []
        
        for _ in range(num_samples):
            attack_type = np.random.choice([at for at in self.attack_types if at != 'normal'])
            category = self.attack_categories.get(attack_type, 'unknown')
            
            if category == 'dos':
                # DoS attacks: high connection counts, similar services
                duration = np.random.exponential(1000)
                protocol = np.random.choice(['tcp', 'udp', 'icmp'], p=[0.6, 0.2, 0.2])
                service = np.random.choice(['http', 'echo', 'private'], p=[0.5, 0.3, 0.2])
                flag = np.random.choice(['SF', 'REJ', 'RSTR'], p=[0.4, 0.3, 0.3])
                
                src_bytes = np.random.lognormal(10, 2)
                dst_bytes = np.random.lognormal(5, 2)
                
                # High connection counts for DoS
                count = np.random.poisson(50)
                srv_count = np.random.poisson(40)
                
                same_srv_rate = np.random.beta(8, 1)  # Very high same service rate
                diff_srv_rate = 1 - same_srv_rate
                
                dst_host_count = np.random.poisson(100)
                dst_host_srv_count = np.random.poisson(80)
                
                dst_host_same_srv_rate = np.random.beta(8, 1)
                dst_host_diff_srv_rate = 1 - dst_host_same_srv_rate
                
                # Higher error rates for DoS
                serror_rate = np.random.beta(3, 2)
                rerror_rate = np.random.beta(3, 2)
                dst_host_serror_rate = np.random.beta(3, 2)
                dst_host_rerror_rate = np.random.beta(3, 2)
                
            elif category == 'probe':
                # Probe attacks: scanning patterns
                duration = np.random.exponential(50)
                protocol = np.random.choice(['tcp', 'icmp'], p=[0.7, 0.3])
                service = np.random.choice(self.services)
                flag = np.random.choice(['SF', 'REJ', 'RSTR'], p=[0.3, 0.4, 0.3])
                
                src_bytes = np.random.lognormal(6, 1)
                dst_bytes = np.random.lognormal(4, 1)
                
                # Moderate connection counts
                count = np.random.poisson(20)
                srv_count = np.random.poisson(15)
                
                same_srv_rate = np.random.beta(2, 3)  # Lower same service rate (scanning different services)
                diff_srv_rate = 1 - same_srv_rate
                
                dst_host_count = np.random.poisson(30)
                dst_host_srv_count = np.random.poisson(20)
                
                dst_host_same_srv_rate = np.random.beta(2, 3)
                dst_host_diff_srv_rate = 1 - dst_host_same_srv_rate
                
                # Moderate error rates
                serror_rate = np.random.beta(2, 3)
                rerror_rate = np.random.beta(2, 3)
                dst_host_serror_rate = np.random.beta(2, 3)
                dst_host_rerror_rate = np.random.beta(2, 3)
                
            elif category == 'r2l':
                # Remote to local attacks
                duration = np.random.exponential(200)
                protocol = 'tcp'
                service = np.random.choice(['ftp', 'telnet', 'smtp', 'pop3', 'imap'])
                flag = 'SF'
                
                src_bytes = np.random.lognormal(7, 1)
                dst_bytes = np.random.lognormal(8, 1)
                
                count = np.random.poisson(5)
                srv_count = np.random.poisson(3)
                
                same_srv_rate = np.random.beta(4, 1)
                diff_srv_rate = 1 - same_srv_rate
                
                dst_host_count = np.random.poisson(10)
                dst_host_srv_count = np.random.poisson(5)
                
                dst_host_same_srv_rate = np.random.beta(4, 1)
                dst_host_diff_srv_rate = 1 - dst_host_same_srv_rate
                
                serror_rate = np.random.beta(1, 10)
                rerror_rate = np.random.beta(1, 10)
                dst_host_serror_rate = np.random.beta(1, 10)
                dst_host_rerror_rate = np.random.beta(1, 10)
                
            else:  # u2r or others
                duration = np.random.exponential(500)
                protocol = 'tcp'
                service = np.random.choice(['http', 'ftp', 'telnet'])
                flag = 'SF'
                
                src_bytes = np.random.lognormal(9, 2)
                dst_bytes = np.random.lognormal(6, 2)
                
                count = np.random.poisson(3)
                srv_count = np.random.poisson(2)
                
                same_srv_rate = np.random.beta(3, 2)
                diff_srv_rate = 1 - same_srv_rate
                
                dst_host_count = np.random.poisson(5)
                dst_host_srv_count = np.random.poisson(3)
                
                dst_host_same_srv_rate = np.random.beta(3, 2)
                dst_host_diff_srv_rate = 1 - dst_host_same_srv_rate
                
                serror_rate = np.random.beta(1, 5)
                rerror_rate = np.random.beta(1, 5)
                dst_host_serror_rate = np.random.beta(1, 5)
                dst_host_rerror_rate = np.random.beta(1, 5)
            
            sample = [
                duration, protocol, service, flag, src_bytes, dst_bytes,
                0, 0, 0, np.random.poisson(2), np.random.poisson(1), 
                np.random.choice([0, 1], p=[0.5, 0.5]),
                np.random.poisson(1), np.random.choice([0, 1], p=[0.9, 0.1]),
                np.random.choice([0, 1, 2], p=[0.8, 0.15, 0.05]), np.random.poisson(1),
                np.random.poisson(1), np.random.poisson(0.5), np.random.poisson(1), 0,
                np.random.choice([0, 1], p=[0.7, 0.3]), np.random.choice([0, 1], p=[0.6, 0.4]),
                count, srv_count, serror_rate, serror_rate, rerror_rate, rerror_rate,
                same_srv_rate, diff_srv_rate, np.random.beta(1, 3),
                dst_host_count, dst_host_srv_count, dst_host_same_srv_rate,
                dst_host_diff_srv_rate, np.random.beta(1, 3), np.random.beta(1, 3),
                dst_host_serror_rate, dst_host_serror_rate, dst_host_rerror_rate,
                dst_host_rerror_rate
            ]
            
            data.append(sample)
        
        return data, [attack_type] * num_samples

    def generate_dataset(self, normal_ratio=0.7):
        """Generate complete dataset with normal and attack traffic"""
        num_normal = int(self.num_samples * normal_ratio)
        num_attack = self.num_samples - num_normal
        
        print(f"Generating {num_normal} normal samples...")
        normal_data = self.generate_normal_traffic(num_normal)
        
        print(f"Generating {num_attack} attack samples...")
        attack_data, attack_types = self.generate_attack_traffic(num_attack)
        
        # Combine data
        all_data = normal_data + attack_data
        labels = ['normal'] * num_normal + attack_types
        
        # Create DataFrame
        df = pd.DataFrame(all_data, columns=self.feature_columns)
        df['label'] = labels
        
        # Add attack category
        df['category'] = df['label'].apply(lambda x: self.attack_categories.get(x, 'unknown'))
        
        return df

    def save_dataset(self, df, filepath='data/nsl_kdd_dataset.csv'):
        """Save dataset to CSV file"""
        df.to_csv(filepath, index=False)
        print(f"Dataset saved to {filepath}")
        print(f"Dataset shape: {df.shape}")
        print(f"Class distribution:")
        print(df['label'].value_counts())
        print(f"Category distribution:")
        print(df['category'].value_counts())

if __name__ == "__main__":
    generator = NSLKDDDataGenerator(num_samples=50000)
    dataset = generator.generate_dataset(normal_ratio=0.6)
    generator.save_dataset(dataset)
