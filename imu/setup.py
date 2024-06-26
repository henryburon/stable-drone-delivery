from setuptools import find_packages, setup

package_name = 'imu'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Henry Buron',
    maintainer_email='henryburon2024@u.northwestern.edu',
    description='This package publishes the IMU data from the BNO085 sensor.',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'bno085 = imu.bno085:bn085_entry'
        ],
    },
)
