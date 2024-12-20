# High-Resolution TMS Grid System with GA-Optimized Design and RL Control Using SimNIBS

## Project Overview
We will make a simulation, leveraging SimNIBS 4.1 for high-fidelity electromagnetic simulations, to create a proposal to the Neural Modeling and Simulation Lab at the University of Southern California. For the development of an adaptive, high-precision transcranial magnetic stimulation (TMS) grid system using Dr. Song's lab's validated C-shaped miniaturized coils. The system combines genetic algorithm (GA) optimization for grid configuration with Soft Actor-Critic (SAC) reinforcement learning for dynamic control of the coordination of the coils in the grid to allow us to encode information directly to the brain.

## Baseline Technology Specifications 
(Based on Jiang et al., 2023, JNE) Lab: https://slab.usc.edu/feat-pub.html

### Single C-Shaped Coil Parameters
- Core dimensions: 4×7 mm
- Iron powder core (μr = 5000)
- Copper wire: 30 turns, insulated
- Validated performance:
  * Maximum magnetic field: 460 mT
  * Induced electric field: 7.2 V/m in brain tissue
  * Demonstrated focal stimulation capability
  * Verified concurrent recording compatibility

### Validated Capabilities
- Focal subthreshold rTMS delivery
- Concurrent electrophysiological recording
- Demonstrated modulation of:
  * Single-unit activities (SUAs)
  * Somatosensory evoked potentials (SSEPs)
  * Motor evoked potentials (MEPs)

## Simulation Framework

### 1. SimNIBS Integration
#### Core Components
- SimNIBS 4.1 FEM solver
- Validated head model (from example dataset)
  * ~5.5M elements
  * High-resolution mesh
  * Accurate tissue boundaries
- Field calculation accuracy: 1e-10
- Isotropic conductivity models

#### Baseline Results (Single Coil)
Latest simulation (standard figure-8):
- Maximum E-field in GM: 1.81 V/m
- Field Distribution:
  * 99.9th percentile: 1.39 V/m
  * 95th percentile: 0.53 V/m
- Stimulation Volumes:
  * 25% threshold: 48,568.50 mm³
  * 50% threshold: 7,945.68 mm³
  * 75% threshold: 799.24 mm³

## Multi-Level Optimization Framework

### 1. GA-SimNIBS Grid Design
#### Chromosome Structure
- Array configuration (3×3 to 5×5)
- Inter-coil spacing (15-35 mm)
- Individual coil parameters:
  * Core orientation
  * Gap width variations
  * Winding patterns
  * Phase relationships

#### Fitness Components
- Field coverage maximization
- Inter-coil interference minimization
- Energy efficiency metrics
- Concurrent recording compatibility
- Thermal management

### 2. SAC-RL Control System
#### State Space
- Multi-unit neural activity
- Current stimulation parameters
- Field distribution patterns
- Thermal state monitoring
- System positioning data

#### Action Space
- Individual coil activations
- Phase relationships
- Amplitude modulation
- Pattern sequencing
- Concurrent recording windows

## SimNIBS Implementation

### 1. Simulation Pipeline
```python
def simulate_grid_configuration(config):
    # Initialize SimNIBS session
    session = sim_struct.SESSION()
    session.fnamehead = 'ernie.msh'
    
    # Set up coil array with Song lab specifications
    tmslist = session.add_tmslist()
    for coil in config['coils']:
        pos = tmslist.add_position()
        pos.coil_design = 'c_shaped'
        pos.dimensions = [4e-3, 7e-3]  # 4x7 mm
        pos.core_mu = 5000  # Iron powder core
        pos.turns = 30
        pos.centre = coil['position']
        pos.pos_ydir = coil['direction']
        pos.didt = coil['intensity']
    
    # Run simulation
    results = run_simnibs(session)
    
    return analyze_field_distribution(results)
```

### 2. Field Analysis
```python
def analyze_field_coverage(results):
    # Extract field data
    e_mag = results.field['magnE'].value * 1e6  # Convert to V/m
    
    # Get tissue-specific results
    gm_mask = results.mesh.elm.tag2 == 2  # Gray matter
    e_mag_gm = e_mag[gm_mask]
    
    # Calculate coverage metrics
    coverage = {
        'max_field': np.max(e_mag_gm),
        'mean_field': np.mean(e_mag_gm),
        'stim_volume': calculate_stim_volume(e_mag_gm, results.mesh, gm_mask)
    }
    
    return coverage
```

## Expected Outcomes

### 1. Hardware Innovation
- Optimized grid configuration using Song lab's coil technology
- Enhanced spatial precision
- Improved concurrent recording
- Efficient thermal management

### 2. Control Capabilities
- Real-time pattern optimization
- Adaptive stimulation protocols
- Safety-constrained operation
- Concurrent recording management

### 3. Clinical Applications
- Enhanced therapeutic targeting
- Precise neuromodulation
- Improved treatment protocols
- Real-time response monitoring

## Implementation Strategy

### Phase 1: Single Coil Validation
1. SimNIBS model of C-shaped coil
2. Field simulation validation
3. Comparison with experimental data
4. Recording compatibility verification

### Phase 2: Grid Optimization
1. GA parameter tuning
2. Pattern library generation
3. Interference mapping
4. Thermal profile optimization

### Phase 3: RL Integration
1. State-space definition
2. Action-space mapping
3. Safety constraint implementation
4. Policy optimization

### Phase 4: System Validation
1. Hardware prototype testing
2. Control system verification
3. Recording quality assessment
4. Safety protocol validation